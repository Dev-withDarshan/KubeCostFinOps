$ErrorActionPreference = "Stop"
try {
    $pptApp = New-Object -ComObject PowerPoint.Application
    $pptxPath = (Resolve-Path "presentation\KubeCostFinOps_Professional_Project_Presentation.pptx").Path
    $pdfPath = [System.IO.Path]::Combine((Get-Location).Path, "presentation\KubeCostFinOps_Presentation.pdf")
    
    Write-Host "Opening presentation: $pptxPath"
    # Parameters: FileName, ReadOnly, Untitled, WithWindow
    $deck = $pptApp.Presentations.Open($pptxPath, 1, 0, 0)
    
    Write-Host "Exporting to PDF: $pdfPath"
    # 32 = ppSaveAsPDF
    $deck.SaveAs($pdfPath, 32)
    $deck.Close()
    $pptApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pptApp) | Out-Null
    Write-Host "SUCCESS: PDF created successfully at $pdfPath"
} catch {
    Write-Host "PDF Export failed: $($_.Exception.Message)"
    exit 1
}

