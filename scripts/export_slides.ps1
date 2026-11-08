$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$inputRoot = Split-Path -Parent $projectRoot
$pptApp = New-Object -ComObject PowerPoint.Application
try {
  Get-ChildItem -LiteralPath $inputRoot -File | Where-Object { $_.Extension -in '.ppt', '.pptx' } | ForEach-Object {
    $number = [int]($_.Name.Split('.')[0])
    $ident = 'm{0:d2}' -f $number
    $deck = $pptApp.Presentations.Open($_.FullName, -1, 0, 0)
    try {
      $pdfPath = Join-Path $projectRoot "public/sources/$ident.pdf"
      $deck.SaveAs($pdfPath, 32)
      $slidePages = @()
      foreach ($slide in $deck.Slides) {
        $slideText = @()
        foreach ($shape in $slide.Shapes) {
          if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) { $slideText += $shape.TextFrame.TextRange.Text }
        }
        $slidePages += @{page=[int]$slide.SlideIndex; text=($slideText -join "`n")}
      }
      $jsonPath = Join-Path $projectRoot "content/$ident.json"
      $doc = Get-Content -LiteralPath $jsonPath -Raw -Encoding utf8 | ConvertFrom-Json
      $doc | Add-Member -NotePropertyName viewFile -NotePropertyValue "sources/$ident.pdf" -Force
      if ($doc.pages.Count -eq 0) { $doc.pages = $slidePages }
      $doc | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $jsonPath -Encoding utf8
      ($doc.pages | ForEach-Object { "=== $($_.page) ===`n$($_.text)" }) -join "`n`n" | Set-Content -LiteralPath (Join-Path $projectRoot "content/$ident.txt") -Encoding utf8
      Write-Output "$ident exported: $($deck.Slides.Count) slides"
    } finally { $deck.Close() }
  }
} finally { $pptApp.Quit() }
