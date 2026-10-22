$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "C:\Users\gnavy\Downloads\KubeCostFinOps\1Submission\FINAL_VERIFIED\BCSE355L_Kubernetes_FinOps_Final_Report.docx"
    $doc = $word.Documents.Open($docPath)
    Write-Host "Total paragraphs: $($doc.Paragraphs.Count)"
    
    foreach ($p in $doc.Paragraphs) {
        $style = $p.Style.NameLocal
        if ($style -like "*Heading 1*") {
            $txt = $p.Range.Text.Trim()
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "Page $page : $txt"
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
