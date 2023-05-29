<?php
include("classes/login_c.php");
$login = new Login();
$user_data = $login->check_login($_SESSION['IOT_userid']);
$USER = $user_data;

if(!(isset($USER))){
  
  header("Location: login.php");
}
 if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $query = "UPDATE Notifications SET seen =".$_POST['seen']." WHERE id =".$_POST['id'];  
    $database = new Database();
    $notifications = $database->save($query);
 }
 ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        .panel{
            margin-top: 100px;
            display: flex;
            flex-direction: column;
        }
        .card{
            padding: 20px;
            width: 90%;
            margin: 0 auto;
            font-size: 20px;
        }
        .appliance{
            display: flex;
            justify-content: space-between;
        }
        .markas{
            display: flex;
            justify-content: flex-end;
            color: black;
            font-size: 14px;
            text-decoration: underline;
        }
    </style>
</head>
<?php
    include("header.php");
    ?>
    <div class="main-panel" id="main-panel">
<?php
   include("navbar.php"); 
   ?>

<div class="panel" id="panel">
<?php
                    $query = "SELECT * FROM Notifications where userid = '$_SESSION[IOT_userid]' ORDER BY seen, id DESC";  
                    $database = new Database();
                    $notifications = $database->read($query);
                ?>
                <?php
                      foreach ($notifications as $key => $value) {
                        if($value['seen'] == 0){
                          echo '<div class="card" href="#" style="background-color:red;">';
                        }
                        else{
                            echo '<div class="card" href="#">';
                        }
                        echo '<div class="appliance">';
                        echo '<div class="appliance_of">';
                        
                          print_r($value['appliance']);
                        echo "</div>";
                        echo '<div class="date">';
                          print_r($value['date']);
                          echo "</div>";
                          echo "</div>";
                          echo "<br>";
                          print_r($value['notification_msg']);
                          if($value['seen'] == 0){
                          echo '<form action="" method="POST" class="markas"><input type="hidden" name="id" value="'.$value["id"].'"><input type="hidden" name="seen" value="1"><input type="submit" value="Mark as Seen"></form>';
                        }
                        else{ 
                          echo '<form action="" method="POST" class="markas"><input type="hidden" name="id" value="'.$value["id"].'"><input type="hidden" name="seen" value="0"><input type="submit" value="Mark as UnSeen"></form>';
                        }
                          echo "</div>";
                            
                      }

                    include("footer.php");

                ?>



</div>
<script>
        var element = document.getElementById("notification");
        element.classList.add("active");
        var panels = document.getElementById("card");
        if(panels == null){
            document.getElementById("main-panel").innerHTML += '<div style="text-align:center;position:absolute;padding: 30px;margin-top: -100px;margin-left: 40%;">No notifications</div>';
        }
</script>
</div>
