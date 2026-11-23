$docxPath = "C:\8051_micro\Final_Report\8051_Microcontroller_PCB_Design_Report.docx"
$pdfPath  = "C:\8051_micro\Final_Report\8051_Microcontroller_PCB_Design_Report.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening document in Word..."
    $doc = $word.Documents.Open($docxPath)
    
    # Locate TOC Marker
    $found = $false
    for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
        $p = $doc.Paragraphs.Item($i)
        if ($p.Range.Text -match "<<TOC_LOCATION_MARKER>>") {
            Write-Host "Found TOC location at paragraph $i. Replacing marker and inserting Table of Contents..."
            $range = $p.Range
            $range.Text = ""
            $toc = $doc.TablesOfContents.Add($range, $true, 1, 3)
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "TOC marker not matched, adding TOC at beginning of body..."
        $p = $doc.Paragraphs.Item(6)
        $toc = $doc.TablesOfContents.Add($p.Range, $true, 1, 3)
    }
    
    # Update TOC and Fields
    Write-Host "Updating Table of Contents and fields..."
    if ($doc.TablesOfContents.Count -gt 0) {
        $doc.TablesOfContents.Item(1).Update()
    }
    
    foreach ($field in $doc.Fields) {
        $field.Update() | Out-Null
    }
    
    # Save the updated DOCX
    Write-Host "Saving finalized DOCX..."
    $doc.Save()
    
    # Export to PDF (17 = wdExportFormatPDF)
    Write-Host "Exporting to PDF: $pdfPath ..."
    $doc.ExportAsFixedFormat(
        $pdfPath,
        17,            # wdExportFormatPDF
        $false,        # OpenAfterExport
        0,             # wdExportOptimizeForPrint
        0,             # wdExportAllDocument
        1,             # From page
        1,             # To page
        0,             # wdExportDocumentContent
        $true,         # IncludeDocProps
        $true,         # KeepIRM
        0,             # wdExportCreateNoBookmarks -> 1 = wdExportCreateHeadingBookmarks
        $true,         # DocStructureTags
        $true,         # BitmapMissingFonts
        $false         # UseISO19005_1 (PDF/A)
    )
    
    Write-Host "Successfully generated PDF report!"
} catch {
    Write-Host "Error in Word processing: " $_.Exception.Message
} finally {
    if ($doc) {
        $doc.Close([ref]$false)
    }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host "Word application closed."
}
