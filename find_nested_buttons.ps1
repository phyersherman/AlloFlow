# Read the full file content
$content = [System.IO.File]::ReadAllText("c:\Users\cabba\OneDrive\Desktop\UDL-Tool-Updated\AlloFlowANTI.txt")

# Build line number lookup: array index = char position -> line number
# (too memory-heavy for 4.5MB file, use a function instead)
function Get-LineNum($pos) {
    return ($content.Substring(0, $pos) -split "`n").Count
}

# Strategy: find all <button that are NOT self-closing
# A <button is self-closing if the next > or /> after it is />
# We need to find the matching > for each <button
$buttonOpenPattern = [regex]'<button[\s>]'
$openMatches = $buttonOpenPattern.Matches($content)

# For each <button, find if it's self-closing or not by scanning forward for the matching >
$nonSelfClosingButtons = @()
foreach ($m in $openMatches) {
    $pos = $m.Index
    # Scan forward from pos to find the end of this tag
    # We need to find > that is not part of JSX expressions inside {}
    $braceDepth = 0
    $i = $pos + 1
    $isSelfClosing = $false
    $tagEnd = -1
    while ($i -lt $content.Length) {
        $ch = $content[$i]
        if ($ch -eq '{') { $braceDepth++ }
        elseif ($ch -eq '}') { $braceDepth-- }
        elseif ($braceDepth -eq 0 -and $ch -eq '>') {
            # Check if previous non-space char is /
            $j = $i - 1
            while ($j -ge $pos -and $content[$j] -match '\s') { $j-- }
            if ($j -ge $pos -and $content[$j] -eq '/') {
                $isSelfClosing = $true
            }
            $tagEnd = $i
            break
        }
        $i++
    }
    
    if (-not $isSelfClosing -and $tagEnd -gt 0) {
        $lineNum = Get-LineNum $pos
        $nonSelfClosingButtons += [PSCustomObject]@{Pos=$pos; Line=$lineNum; TagEnd=$tagEnd}
    }
}

Write-Output "Found $($nonSelfClosingButtons.Count) non-self-closing <button> tags"

# Now find all </button> tags
$closePattern = [regex]'</button>'
$closeMatches = $closePattern.Matches($content)

# Build sorted event list
$events = @()
foreach ($btn in $nonSelfClosingButtons) {
    $events += [PSCustomObject]@{Type='open'; Pos=$btn.Pos; Line=$btn.Line}
}
foreach ($m in $closeMatches) {
    $lineNum = Get-LineNum $m.Index
    $events += [PSCustomObject]@{Type='close'; Pos=$m.Index; Line=$lineNum}
}

$events = $events | Sort-Object Pos

# Walk through events tracking depth
$depth = 0
$stack = @()
$found = @()
foreach ($ev in $events) {
    if ($ev.Type -eq 'open') {
        $depth++
        $stack += $ev.Line
        if ($depth -ge 2) {
            $parentLine = $stack[$stack.Count - 2]
            $found += "NESTED BUTTON: child at line $($ev.Line), parent at line $parentLine (depth=$depth)"
        }
    } elseif ($ev.Type -eq 'close') {
        $depth = [Math]::Max(0, $depth - 1)
        if ($stack.Count -gt 0) { 
            $stack = @($stack[0..([Math]::Max(0, $stack.Count-2))])
        }
    }
}

if ($found.Count -eq 0) {
    Write-Output "No nested buttons found!"
} else {
    foreach ($f in $found) {
        Write-Output $f
    }
}
Write-Output "Final depth: $depth (should be 0 if balanced)"
