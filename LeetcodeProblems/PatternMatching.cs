using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using HtmlAgilityPack;
using UglyToad.PdfPig;

public class PatternMatching
{
    public static async Task PrintGridFromGoogleDoc(string googleDocUrl)
    {
        try
        {
            // 1) Try plain text
            try
            {
                string txtUrl = ConvertToExportUrl(googleDocUrl, ExportFormat.Txt);
                Console.WriteLine($"Trying TXT: {txtUrl}");
                string content = await FetchDocumentContent(txtUrl);
                var grid = ParseGridData(content);
                if (grid.Count > 0)
                {
                    Console.WriteLine("Parsed grid from TXT export.");
                    PrintGrid(grid);
                    return;
                }
                else
                {
                    Console.WriteLine("No valid grid found in TXT export.");
                }
            }
            catch (Exception exTxt)
            {
                Console.WriteLine($"TXT export failed: {exTxt.Message}");
            }

            // 2) Try HTML
            try
            {
                string htmlUrl = ConvertToExportUrl(googleDocUrl, ExportFormat.Html);
                Console.WriteLine($"Trying HTML: {htmlUrl}");
                string html = await FetchDocumentContent(htmlUrl);
                var gridFromHtml = ParseGridFromHtml(html);
                if (gridFromHtml.Count > 0)
                {
                    Console.WriteLine("Parsed grid from HTML export.");
                    PrintGrid(gridFromHtml);
                    return;
                }
                else
                {
                    Console.WriteLine("No valid grid found in HTML export. Falling back to text extraction from HTML.");
                    // fallback: attempt plain-text extraction from HTML body
                    var asText = HtmlToPlainText(html);
                    var fallbackGrid = ParseGridData(asText);
                    if (fallbackGrid.Count > 0)
                    {
                        Console.WriteLine("Parsed grid from HTML->text fallback.");
                        PrintGrid(fallbackGrid);
                        return;
                    }
                }
            }
            catch (Exception exHtml)
            {
                Console.WriteLine($"HTML export failed: {exHtml.Message}");
            }

            // 3) Try PDF (last resort)
            try
            {
                string pdfUrl = ConvertToExportUrl(googleDocUrl, ExportFormat.Pdf);
                Console.WriteLine($"Trying PDF: {pdfUrl}");
                byte[] pdfBytes = await FetchBinaryContent(pdfUrl);
                string extractedText = ExtractTextFromPdfBytes(pdfBytes);
                var gridFromPdf = ParseGridData(extractedText);
                if (gridFromPdf.Count > 0)
                {
                    Console.WriteLine("Parsed grid from PDF export.");
                    PrintGrid(gridFromPdf);
                    return;
                }
                else
                {
                    Console.WriteLine("No valid grid found in PDF export text.");
                }
            }
            catch (Exception exPdf)
            {
                Console.WriteLine($"PDF export failed: {exPdf.Message}");
            }

            Console.WriteLine("No valid grid data found after trying TXT, HTML and PDF exports.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Fatal error: {ex.Message}");
        }
    }

    // ---------- Export URL builders ----------
    private enum ExportFormat { Txt, Html, Pdf }

    private static string ConvertToExportUrl(string googleDocUrl, ExportFormat format)
    {
        if (string.IsNullOrWhiteSpace(googleDocUrl))
            throw new ArgumentException("Google Docs URL is empty", nameof(googleDocUrl));

        // If already looks like an export URL, accept it
        if (googleDocUrl.Contains("/export") ||
            googleDocUrl.Contains("format=txt") ||
            googleDocUrl.Contains("format=html") ||
            googleDocUrl.Contains("format=pdf") ||
            googleDocUrl.Contains("output=txt") ||
            googleDocUrl.Contains("output=html") ||
            googleDocUrl.Contains("output=pdf"))
        {
            return googleDocUrl;
        }

        string fmtTxt = format == ExportFormat.Txt ? "txt" : (format == ExportFormat.Html ? "html" : "pdf");

        // Published-to-web URL /d/e/<pubId>/pub  (use output=<fmt>)
        var mPub = Regex.Match(googleDocUrl, @"/d/e/([a-zA-Z0-9\-_]+)");
        if (mPub.Success)
        {
            var pubId = mPub.Groups[1].Value;
            return $"https://docs.google.com/document/d/e/{pubId}/pub?output={fmtTxt}";
        }

        // Standard doc URL /d/<docId>/...
        var mDoc = Regex.Match(googleDocUrl, @"/d/([a-zA-Z0-9\-_]+)");
        if (mDoc.Success)
        {
            var docId = mDoc.Groups[1].Value;
            return $"https://docs.google.com/document/d/{docId}/export?format={fmtTxt}";
        }

        // Query-style link with ?id=<docId>
        var mQueryId = Regex.Match(googleDocUrl, @"[?&]id=([a-zA-Z0-9\-_]+)");
        if (mQueryId.Success)
        {
            var docId = mQueryId.Groups[1].Value;
            return $"https://docs.google.com/document/d/{docId}/export?format={fmtTxt}";
        }

        throw new ArgumentException("Invalid Google Docs URL format");
    }

    // ---------- Fetch helpers ----------
    private static async Task<string> FetchDocumentContent(string url)
    {
        using var client = new HttpClient();
        client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (compatible; GoogleDocGridParser/1.0)");
        var resp = await client.GetAsync(url);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsStringAsync();
    }

    private static async Task<byte[]> FetchBinaryContent(string url)
    {
        using var client = new HttpClient();
        client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (compatible; GoogleDocGridParser/1.0)");
        var resp = await client.GetAsync(url);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadAsByteArrayAsync();
    }

    // ---------- HTML parsing ----------
    private static Dictionary<(int x, int y), char> ParseGridFromHtml(string html)
    {
        var grid = new Dictionary<(int x, int y), char>();
        var doc = new HtmlDocument();
        doc.LoadHtml(html);

        var tables = doc.DocumentNode.SelectNodes("//table");
        if (tables != null)
        {
            foreach (var table in tables)
            {
                // Try row-by-row parsing first (tr -> td)
                var rows = table.SelectNodes(".//tr");
                if (rows != null)
                {
                    bool anyRowParsed = false;
                    foreach (var tr in rows)
                    {
                        var cells = tr.SelectNodes(".//td|.//th");
                        if (cells != null && cells.Count >= 3)
                        {
                            string a = CleanText(cells[0].InnerText);
                            string b = CleanText(cells[1].InnerText);
                            string c = CleanText(cells[2].InnerText);
                            if (int.TryParse(a, out int x) && !string.IsNullOrEmpty(b) && int.TryParse(c, out int y))
                            {
                                grid[(x, y)] = b[0];
                                anyRowParsed = true;
                            }
                        }
                    }
                    if (anyRowParsed && grid.Count > 0)
                        return grid;
                }

                // If rows had 1 cell each or row-style failed, try sequential cell grouping
                var allCells = table.SelectNodes(".//td|.//th");
                if (allCells != null && allCells.Count >= 3)
                {
                    var texts = allCells.Select(n => CleanText(n.InnerText)).Where(s => !string.IsNullOrWhiteSpace(s)).ToList();
                    for (int i = 0; i + 2 < texts.Count; i += 3)
                    {
                        if (int.TryParse(texts[i], out int x) && !string.IsNullOrEmpty(texts[i + 1]) && int.TryParse(texts[i + 2], out int y))
                        {
                            grid[(x, y)] = texts[i + 1][0];
                        }
                    }
                    if (grid.Count > 0) return grid;
                }
            }
        }

        // Fallback: extract plain text from HTML and try ParseGridData on it
        var text = HtmlToPlainText(html);
        return ParseGridData(text);
    }

    private static string CleanText(string s)
    {
        if (s == null) return string.Empty;
        return Regex.Replace(s, @"\s+", " ").Trim();
    }

    private static string HtmlToPlainText(string html)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);
        // Use InnerText; it tends to flatten markup but preserve table cell order in many cases
        return doc.DocumentNode.InnerText ?? string.Empty;
    }

    // ---------- PDF extraction ----------
    private static string ExtractTextFromPdfBytes(byte[] pdfBytes)
    {
        using var ms = new MemoryStream(pdfBytes);
        using var pdf = PdfDocument.Open(ms);
        var pages = pdf.GetPages();
        var sb = new System.Text.StringBuilder();
        foreach (var p in pages)
        {
            // PdfPig provides page.Text
            sb.AppendLine(p.Text);
        }
        return sb.ToString();
    }

    // ---------- Text parsing (robust) ----------
    private static Dictionary<(int x, int y), char> ParseGridData(string content)
    {
        var gridData = new Dictionary<(int x, int y), char>();
        if (string.IsNullOrWhiteSpace(content)) return gridData;

        // Normalize newlines and split, removing empty lines but preserving useful data
        var lines = content
            .Replace("\r\n", "\n")
            .Replace('\r', '\n')
            .Split('\n', StringSplitOptions.RemoveEmptyEntries)
            .Select(l => l.Trim())
            .Where(l => !string.IsNullOrEmpty(l))
            .ToList();

        // Locate start after header "x-coordinate" if present
        int headerIndex = lines.FindIndex(l => l.IndexOf("x-coordinate", StringComparison.OrdinalIgnoreCase) >= 0);
        if (headerIndex >= 0)
        {
            lines = lines.Skip(headerIndex + 1).ToList();
        }

        // iterate lines; support both row style and stacked (3 lines per record)
        for (int i = 0; i < lines.Count;)
        {
            string line = lines[i];

            // Attempt row-style: "27   █   0"
            string[] parts = Regex.Split(line, @"\s{2,}|\t");
            if (parts.Length >= 3)
            {
                if (int.TryParse(parts[0].Trim(), out int x) &&
                    !string.IsNullOrEmpty(parts[1].Trim()) &&
                    int.TryParse(parts[2].Trim(), out int y))
                {
                    gridData[(x, y)] = parts[1].Trim()[0];
                }
                i++;
                continue;
            }

            // Attempt stacked-style: next three lines are x, char, y
            if (i + 2 < lines.Count)
            {
                string a = lines[i];
                string b = lines[i + 1];
                string c = lines[i + 2];
                if (int.TryParse(a, out int x2) && !string.IsNullOrEmpty(b) && int.TryParse(c, out int y2))
                {
                    gridData[(x2, y2)] = b[0];
                    i += 3;
                    continue;
                }
            }

            // If nothing matched, move forward one line
            i++;
        }

        return gridData;
    }

    // ---------- Print grid ----------
    private static void PrintGrid(Dictionary<(int x, int y), char> gridData)
    {
        if (gridData.Count == 0)
        {
            Console.WriteLine("No valid grid data found.");
            return;
        }

        int minX = int.MaxValue, maxX = int.MinValue;
        int minY = int.MaxValue, maxY = int.MinValue;

        foreach (var kvp in gridData)
        {
            int x = kvp.Key.x;
            int y = kvp.Key.y;

            minX = Math.Min(minX, x);
            maxX = Math.Max(maxX, x);
            minY = Math.Min(minY, y);
            maxY = Math.Max(maxY, y);
        }

        for (int y = minY; y <= maxY; y++)
        {
            for (int x = minX; x <= maxX; x++)
            {
                if (gridData.TryGetValue((x, y), out char ch))
                {
                    Console.Write(ch);
                }
                else
                {
                    Console.Write(' ');
                }
            }
            Console.WriteLine();
        }
    }
}
