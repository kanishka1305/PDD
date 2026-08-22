Start-Sleep -Seconds 5
$pages = @("/login","/dashboard","/upload","/refine","/workflow","/history","/results")
foreach ($p in $pages) {
    try {
        $code = (Invoke-WebRequest -Uri "http://localhost:8000$p" -UseBasicParsing).StatusCode
        Write-Host "OK  $p -> $code"
    } catch {
        Write-Host "ERR $p -> $_"
    }
}
$apis = @("/health","/stl-region/1/condyles","/export-dicom/1/condyles")
foreach ($a in $apis) {
    try {
        $r = Invoke-WebRequest -Uri "http://localhost:8000$a" -UseBasicParsing
        Write-Host "OK  $a -> $($r.StatusCode)"
    } catch {
        Write-Host "ERR $a -> $_"
    }
}
