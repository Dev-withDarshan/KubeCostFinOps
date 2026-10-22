$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "C:\Users\gnavy\Downloads\KubeCostFinOps\1Submission\FINAL_VERIFIED\BCSE355L_Kubernetes_FinOps_Final_Report.docx"
    $pdfPath = "C:\Users\gnavy\Downloads\KubeCostFinOps\1Submission\FINAL_VERIFIED\BCSE355L_Kubernetes_FinOps_Final_Report.pdf"
    $doc = $word.Documents.Open($docPath)
    # wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $pageCount = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "Exported to $pdfPath successfully. Total pages: $pageCount"
    $doc.Close([ref]$false)

    # Also synchronize all PDF targets
    Copy-Item -Path $pdfPath -Destination "C:\Users\gnavy\Downloads\KubeCostFinOps\1Submission\BCSE355L_Kubernetes_FinOps_Final_Report.pdf" -Force
    Copy-Item -Path $pdfPath -Destination "C:\Users\gnavy\Downloads\KubeCostFinOps\1Submission\BCSE355L_Final_Project_Report_K_Darshan.pdf" -Force
    Copy-Item -Path $pdfPath -Destination "C:\Users\gnavy\Downloads\KubeCostFinOps\BCSE355L_Kubernetes_FinOps_Final_Report.pdf" -Force
    Write-Host "Synchronized all PDF targets successfully."
} finally {
    $word.Quit()
}
