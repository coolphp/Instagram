<?php



$ini = parse_ini_file('../config/config.ini');

$utmz = $_COOKIE['__utmz'];
$phone = $_POST['phone'];
$email = $_POST['name'];
$mail = $_POST['mail'];
$instagram = $_POST['instagram'];
$whatsapp = $_POST['whatsapp'];
$skype = $_POST['skype'];
$info = $_POST['info'];
$utmz = explode(".", $utmz);
$utmz = array_pop($utmz);
$utmz = explode('|', $utmz);
$utmz_out = array();
foreach ($utmz as &$part) {
	$part = explode('=', $part);
	$utmz_out[$part[0]] = $part[1];
}

$mail_title = 'Заявка на товар';

$mail = "
	<html>
		<head>
		  <title>{$mail_title}</title>
		</head>
		<body style='color:#111; font-family:13px Tahoma, Arial, sans-serif;'>
			<p><strong>{$mail_title}<strong></p>
			<p>Ваше Имя: {$_POST['name']}</p>
			<p>Номер: {$_POST['phone']}</p>
			<p>Email: {$_POST['mail']}</p>
			<p>Instagram: {$_POST['instagram']}</p>
			<p>Whatsapp: {$_POST['whatsapp']}</p>
			<p>Skype: {$_POST['skype']}</p>
			<p>Дополнительная информация: {$_POST['info']}</p>
		</body>
	</html>
";

$headers = 'Content-type: text/html; charset=utf-8' . "\r\n" .
		'From: Заказ на товар <'.$ini['from_email'].'>' . "\r\n";

mail($ini['request_email'], $mail_title . ' ' . date('d-m-Y H:i:s'), $mail, $headers);

if(isset($_COOKIE["adpro"])){
	
	header("Location: /success.htm?hash={$hash}");
}else{
	header("Location: /success.htm");
}