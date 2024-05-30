<?php
$servername = "";
$username = "";
$password = "";
$dbname = "";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
    die("Connexió fallida: " . mysqli_connect_error());
}

$sql = "SELECT * FROM preuscat_afiliacio.preuscatafiliat";
$result = mysqli_query($conn, $sql);

if (isset($_GET['asin'])) {
    $asinenviat = $_GET['asin'];
}
else {
    $asinenviat = 'NO VALOR';
}
if (isset($_GET['plataforma'])) {
    $plataformaenviat = $_GET['plataforma'];
}
else {
    $plataformaenviat = 'NO VALOR';
}
if (isset($_GET['price'])) {
    $preuenviat = $_GET['price'];
}
else {
    $preuenviat = 'NO VALOR';
}
if (isset($_GET['desc'])) {
    $descenviat = $_GET['desc'];
}
else {
    $descenviat = 'NO VALOR';
}
$data = date("Y/m/d");

date_default_timezone_set('Europe/Barcelona');
$hora = date('H:i:s');


if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $idprimary = $row["id"] + 1;
    }
}


$sql = "INSERT INTO preuscatafiliat (id, asin, data, hora, plataforma, preu, descompte) VALUES ('$idprimary', '$asinenviat', '$data', '$hora', '$plataformaenviat', '$preuenviat', '$descenviat')";


if (mysqli_query($conn, $sql)) {

} else {

}

mysqli_close($conn);

header("Location: https://amazon.es/dp/".$asinenviat."?tag=p2g8gsdf3t-21 ");
?>
