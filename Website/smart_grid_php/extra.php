<?php
include("classes/login_c.php");
if(!(isset($_SESSION['IOT_userid']))){
    header("Location: login.php");
    die;
}
$login = new Login();
$user_data = $login->check_login($_SESSION['IOT_userid']);
$USER = $user_data;

if(!(isset($USER))){
  
  header("Location: login.php");
}

?>
<!DOCTYPE html>
<html lang="en">

<?php
    include("header.php");
    ?>
    <div class="main-panel">
 <?php
    include("navbar.php"); 
    ?>

<div class="" style="margin-left: 5%;margin-top: 200px;">
<a href="http://127.0.0.1:5000/" style="text-align: center;">OM2M Implementation</a>

<?php include("footer.php"); ?>
<script>
        var element = document.getElementById("extra");
        element.classList.add("active");
</script>
</div>
