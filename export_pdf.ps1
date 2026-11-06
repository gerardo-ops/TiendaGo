$ErrorActionPreference = "Stop"
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $inDoc = (Resolve-Path "Reporte_de_Ejecucion_de_Pruebas_TiendaGo.docx").Path
    $doc = $word.Documents.Open($inDoc)
    $pages = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "Total Pages in Word: $pages"
    $pdfPath = [System.IO.Path]::ChangeExtension($inDoc, ".pdf")
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    $word.Quit()
    Write-Host "PDF successfully exported to: $pdfPath"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
