<?php
include("classes/login_c.php");
$login = new Login();
$user_data = $login->check_login($_SESSION['IOT_userid']);
// print_r($user_data);
// print_r($user_data);
 $USER = $user_data;
 
 if(!(isset($USER))){

    header("Location: login.php");
 }

?>
<html lang="en">
<?php
    include("header.php");
?>
<head>
    <link rel="stylesheet" type="text/css" href="styles/health.css">
     <meta http-equiv="refresh" content="30">
</head>
<div class="main-panel">
    <?php include("navbar.php"); ?>
    <h1 style="margin-top: 100px;">Statistics of Components</h1>
    <div id="healthDataContainer">
    <?php
        for ($i=1; $i < $user_data['field_no']; $i++) { 
            echo '<div class="healthData"><span id="healthlabel'.$i.'"></span><span style="margin-left: 5vw;" id="recentValue'.$i.'"></span><br>
            <script>
        fetch("https://api.thingspeak.com/channels/'.$user_data['channel_id'].'/fields/'.$i.'.json?api_key='.$user_data['Read_Api'].'&results=1", {
    method: "GET",
    headers: {
        "Accept": "application/json",
    },
})
   .then(response => response.json())
   .then(response => 
   {
      document.getElementById("healthlabel'.$i.'").innerHTML = "Plot for : "+JSON.stringify(response["channel"]["field'.$i.'"]).replace(/"/g, "");
      document.getElementById("recentValue'.$i.'").innerHTML = "Recent Reading : "+JSON.stringify(response["feeds"][0]["field'.$i.'"]).replace(/"/g, "");
      
   });
      </script>
            <iframe width="100%" height="240" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/';
            echo $user_data["channel_id"];
            echo '/charts/'.$i.'?api_key=EFISS04IFA6364N9&width=auto&color=00FFFF&results=10"></iframe></div>';
        }
    ?>
    </div>
<?php include("footer.php"); ?>
</div>
<script>
        var element = document.getElementById("statistics");
        element.classList.add("active");
</script>
