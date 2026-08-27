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

if($_SERVER['REQUEST_METHOD'] == 'POST')
{
     $login = new Login();
     if($_POST['prior'] == 1){
        $priority = 12;         
     }
     else{
         $priority = 21;
     }
     $useri = $USER['userid'];
     $query = "UPDATE Users SET priority = '$priority' WHERE userid = '$useri'";
     $DB = new Database();
	 $DB->save($query);
     
     
}
$list = ["MOTORS","LEDS"]
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
<head>

  <style>
    body {
      font-family: Arial, sans-serif;
    }
    .container {
      max-width: 400px;
      margin: 0 auto;
      padding: 20px;
      border: 1px solid #ccc;
    }
    h1 {
      margin-top: 0;
    }
    label {
      display: block;
      margin-bottom: 5px;
    }
    input[type="text"] {
      width: 100%;
      padding: 5px;
      margin-bottom: 10px;
    }
    select {
      width: 100%;
      padding: 5px;
      margin-bottom: 10px;
    }
    button {
      padding: 10px 20px;
      background-color: #4CAF50;
      color: #fff;
      border: none;
      cursor: pointer;
    }
  </style>
</head>
  <div class="container">
    <h1>Settings</h1>
    <label for="username">Username:</label>
    <input type="text" id="username" value="<?php echo $USER['username']   ?>" disabled>
    <br>
    <label for="current-priority">Current Priority Order:</label>
    
    <?php echo $list[$user_data['priority'][0]-1] ?>
    <br>
     <?php echo $list[$user_data['priority'][1]-1] ?>
    <br>
    <h2>Change Priority Order:</h2>
    Selecting Motor priority will decide other:
    <form id="priority-form" method="POST" action="">
      <label for="preference1">MOTOR:</label>
      <select id="preference1" name="prior">
        <option value="1">1</option>
        <?php if($user_data['priority'][0] == 2){
    
                $second = "<option value='2' selected>2</option>";
          }
          else{
    
              $second = "<option value='2'>2</option>";
          }
          
        echo $second;
          ?>
      </select>
      <br>
      <br>
      <!-- Add more preferences here -->
      
      <br>
      <button type="submit">Submit</button>
    </form>
  </div>

 

<?php include("footer.php"); ?>
<script>
        var element = document.getElementById("user");
        element.classList.add("active");
</script>
</div>
