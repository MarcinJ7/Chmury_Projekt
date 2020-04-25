
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
$file_destination= $target_dir.$file_name;
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}

if (file_exists($file_destination)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}

if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}

if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";

} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $file_destination)) {
        echo "<br>The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.<br>";
        echo '<img id="blah" src="'.$dir.$file_name.'" alt="your image" />';
    } else {
        echo "Sorry, there was an error uploading your file.";
	print_r($_FILES);
    }
}
?>
