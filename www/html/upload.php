
<!DOCTYPE html>
<html>

<head>
	<meta charset="UTF-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<meta name="author" content="Marek Knosala" />
	
	<title>AI</title>

    <link rel="stylesheet" href="styles.css">
<link href='http://fonts.googleapis.com/css?family=Lato|Josefin+Sans&subset=latin,latin-ext' rel='stylesheet' type='text/css'>

    <title>Check your age</title>
</head>

<body>
    <div id="wrapper">
		<div id="header">
			<div id="logo">
				Check <span style="color: red;">your</span> age with <span style="color: red;">AI</span>
			</div>
		</div>
		<div id="content">	
		
			<div class="frame">
<?php
function getUserIpAddr(){
    if(!empty($_SERVER['HTTP_CLIENT_IP'])){
        
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    }elseif(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){
        
        $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    }else{
        $ip = $_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}

$d=strtotime("tomorrow");

$main_dir = "/var/www/html/";
$dir = "upload/";
$target_dir = $main_dir.$dir;
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$file_name = date('Y-m-d_H-i-s').'_'.getUserIpAddr().'_'.basename($_FILES["fileToUpload"]["name"]);
$file_name = str_replace(' ', '', $file_name);
$file_name = preg_replace('/\s+/', ' ', $file_name);
$file_destination= $target_dir.$file_name;
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

$msg = "";

if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        $msg = $msg."File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        $msg = $msg."File is not an image.";
        $uploadOk = 0;
    }
}

if (file_exists($file_destination)) {
    $msg = $msg."Sorry, file already exists.";
    $uploadOk = 0;
}

if ($_FILES["fileToUpload"]["size"] > 500000) {
    $msg = $msg."Sorry, your file is too large.";
    $uploadOk = 0;
}

if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
    $msg = $msg."Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    $msg = $msg."Sorry, your file was not uploaded.";

} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $file_destination)) {
        $msg = $msg."<br>The file \"". basename( $_FILES["fileToUpload"]["name"]). "\" has been uploaded.<br>";
        //echo '<img id="blah" src="'.$dir.$file_name.'" alt="your image" />';
    } else {
        $msg = $msg."Sorry, there was an error uploading your file.";
	print_r($_FILES);
    }
}



#$accesskey = "MoV/Ymq3ihTLc9MjWWT945CQvL4ShLNr1fwU7GGXDFTcW19vC1/X3rfGQGPaSeUtSyd6vdtfMIQKXbiJvq5XAg==";
$accesskey = "LICebmDrCg3c4RQPd0dyLwNeBC01x3YlVGdkZ+mR2tAgza8SP/5+UJbKPE7ZLAnHNduYzc6gxVCvsYniB4J2jg==";
#$storageAccount = 'rvbc';
$storageAccount = 'blobprojekt';
$filetoUpload = realpath('./'.$dir.$file_name);
$containerName = 'zdjecia';
$blobName = $file_name;

$destinationURL = "https://$storageAccount.blob.core.windows.net/$containerName/$blobName";

function uploadBlob($filetoUpload, $storageAccount, $containerName, $blobName, $destinationURL, $accesskey) {

    $currentDate = gmdate("D, d M Y H:i:s T", time());
    $handle = fopen($filetoUpload, "r");
    $fileLen = filesize($filetoUpload);

    $headerResource = "x-ms-blob-cache-control:max-age=3600\nx-ms-blob-type:BlockBlob\nx-ms-date:$currentDate\nx-ms-version:2015-12-11";
    $urlResource = "/$storageAccount/$containerName/$blobName";

    $arraysign = array();
    $arraysign[] = 'PUT';               /*HTTP Verb*/  
    $arraysign[] = '';                  /*Content-Encoding*/  
    $arraysign[] = '';                  /*Content-Language*/  
    $arraysign[] = $fileLen;            /*Content-Length (include value when zero)*/  
    $arraysign[] = '';                  /*Content-MD5*/  
    $arraysign[] = 'image/png';         /*Content-Type*/  
    $arraysign[] = '';                  /*Date*/  
    $arraysign[] = '';                  /*If-Modified-Since */  
    $arraysign[] = '';                  /*If-Match*/  
    $arraysign[] = '';                  /*If-None-Match*/  
    $arraysign[] = '';                  /*If-Unmodified-Since*/  
    $arraysign[] = '';                  /*Range*/  
    $arraysign[] = $headerResource;     /*CanonicalizedHeaders*/
    $arraysign[] = $urlResource;        /*CanonicalizedResource*/

    $str2sign = implode("\n", $arraysign);

    $sig = base64_encode(hash_hmac('sha256', urldecode(utf8_encode($str2sign)), base64_decode($accesskey), true));  
    $authHeader = "SharedKey $storageAccount:$sig";

    $headers = [
        'Authorization: ' . $authHeader,
        'x-ms-blob-cache-control: max-age=3600',
        'x-ms-blob-type: BlockBlob',
        'x-ms-date: ' . $currentDate,
        'x-ms-version: 2015-12-11',
        'Content-Type: image/png',
        'Content-Length: ' . $fileLen
    ];

    $ch = curl_init($destinationURL);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($ch, CURLOPT_INFILE, $handle); 
    curl_setopt($ch, CURLOPT_INFILESIZE, $fileLen); 
    curl_setopt($ch, CURLOPT_UPLOAD, true); 
    $result = curl_exec($ch);

    //echo ('Result<br/>');
   // print_r($result);

    //echo ('Error<br/>');
   // print_r(curl_error($ch));

    curl_close($ch);
}

uploadBlob($filetoUpload, $storageAccount, $containerName, $blobName, $destinationURL, $accesskey);


   
// Use unlink() function to delete a file  
#if (!unlink($file_destination)) {  
#    echo ("$file_destination cannot be deleted due to an error");  
#}  
#else {  
#    echo ("$file_destination has been deleted");  
#}  
echo("<div class=\"image\">");
echo("<img src=\"".$dir.$file_name."\" />");
echo("</div>");


echo("<div class=\"starttext\">");
echo("<h3>Result</h3>");
echo("<p>");
echo($msg);
echo("</p>");
echo("</div>");

?>
			</div>
			
			<div class="dottedline"></div>
			
			<div class="frame">
				<div class="starttext" id="about">
					<h3>About</h3>
					<p>This student project was created by: Malwina Kubas, Magdalena Kuna, Marcin Jurczak, Marek Knosala, Edward Sucharda </p>
				</div>
			</div>
			
		</div>
		<div id="footer">
			&copy;2020 Marek Knosala <span style="color: red;"><i class="demo-icon icon-emo-devil">&#xe805;</i></span>
		</div>
	</div>

</body>

</html>
