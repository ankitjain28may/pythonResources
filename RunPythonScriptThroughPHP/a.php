<?php
// $out = shell_exec("python3 -u a.py");
// echo $out;
ob_start();
$handle = popen("python3 -u a.py", 'r');
while(!feof($handle)) {
    $buffer = fgets($handle);
    echo $buffer;
    ob_flush();
}
pclose($handle)

?>