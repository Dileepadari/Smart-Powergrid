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
if($user_data['user_type'] == 'admin'){
  header("Location: admin_index.php");
  die;
}
?>
<!DOCTYPE html>
<html lang="en">
  <style>
    .state{
      display: flex;
      overflow: hidden; 
    }
    .button{
      display: flex;
      background-color: #1abc9c;
      color:white;
      height: 80px;
      padding: 20px;
      text-decoration: none;
      font-size: 25px;
   cursor: pointer;
   margin: 0 1vw;  
   border-radius: 4px;
  } 
  .button-on:hover,
  .button-off:hover{background-color: black;}
  
  </style>
<?php include("header.php");  ?>
<div class="main-panel">
  <!-- Navbar -->
  
  <?php include("navbar.php");  ?>
      <div class="content">
        <br><br>

        <div class="row" >
        <div class="col-md-12" id="rowe">
          <br>
          <h3>User Controls</h3>
          
        </div>
      </div>
    </div>
    <script>
      var values;
      function send_command(api, row, col, val){ 
        console.log(values);
        dup = values[row].split(",");
        dup[col] = val;
        var dup_str = dup.toString();
        values[row] = dup_str; 
        var str = values.join(':');
        console.log(str);
        link = "https://api.thingspeak.com/update?api_key="+api+"&field<?php echo $user_data['field_no'] ?>="+str+"";
        console.log(link);
            fetch(link, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
      } 
      function get_vals(array){
        fetch("https://api.thingspeak.com/channels/<?php echo $user_data['channel_id'] ?>/fields/<?php echo $user_data['field_no'] ?>.json?api_key=<?php echo $user_data['Read_Api'] ?>&results=1", {
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                    },
                })
                   .then(response => response.json())
                   .then(response => 
                   {
                    var string = response["feeds"][0]["field<?php echo $user_data['field_no'] ?>"];
                    values = string.split(":");
                    calculatechart(array, values);
                  });  

      }
                      function calculatechart(array, values){
                        var $i = 0;
                        var arrayconfig = []
                        array.forEach(element => {
                          
                          // console.log(values[$i++]);
                          document.getElementById("rowe").innerHTML+= `<div class="card "  style="background-color: white;">
            <div class="card-header"> 
              <h2 class="card-title col-11">`+element+`</h2>
            </div>
            <div class="card-body">
               
              <h3 class="col-12">State : <span id="`+element+`_state_status">ON</span></h3>
              <h3 class="speed col-12" id="`+element+`_speed">Speed : <span id="`+element+`_speed_status"> 230kmph</span></h3>
              <h3 class="col-12" id="`+element+`_dir">Direction : <span id="`+element+`_direction_status">Clockwise</span></h3>
              <div class="state" id="`+element+`_state">
                <h3 style="padding: 20px;">Switch State : </h3>
                <button class="button button-on" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,0,1)">ON</button>
                <button class="button button-off" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,0,0)" >OFF</button>
              </div>
              <div class="speed state" id="`+element+`_speede">
              <h3 style="padding: 20px;">Switch speed : </h3>
                <button class="button button-on" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,1,0)">Low</button>
                <button class="button button-off" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,1,1)">Average</button>
                <button class="button button-off" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,1,2)"">High</button>
              </div>
              <div class="direction state" id="`+element+`_direction">
              <h3 style="padding: 20px;">Switch direction : </h3>
                <button class="button button-on" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,2,0)">Clockwise</button>
                <button class="button button-off" onclick="send_command('<?php echo$user_data['Write_Api']?>',`+$i+`,2,1)">Anti-CLockwise</button>
              </div>
    
              </div>`;
          
              if(values[$i][0] == 0){
                console.log(values[$i][2]);
                document.getElementById(element+"_state_status").innerHTML = "OFF";
              }
              else{
                document.getElementById(element+"_state_status").innerHTML = "ON";
              }
              if(values[$i][2] == 0){
                console.log(values[$i][0]);
                document.getElementById(element+"_speed_status").innerHTML = "Low";
              }
              else if(values[$i][2] == 1){
                document.getElementById(element+"_speed_status").innerHTML = "Average";
              }
              else{
                document.getElementById(element+"_speed_status").innerHTML = "High";
              }
              if(values[$i][4] == 0){
                document.getElementById(element+"_direction_status").innerHTML = "ClockWise";
              }
              else{
                document.getElementById(element+"_direction_status").innerHTML = "AnticlockWise";
              }
              
              if (element.includes("LED") === true || element.includes("Buzzer") === true ) {
                  document.getElementById(element+"_speed").style.display = 'none';
                  document.getElementById(element+"_dir").style.display = 'none';
                  document.getElementById(element+"_speede").style.display = 'none';
                  document.getElementById(element+"_direction").style.display = 'none';

                  }
                $i++;
            });
                      }
              var array = [];
                    fetch("https://api.thingspeak.com/channels/<?php echo $user_data['channel_id'] ?>/fields/1.json?api_key=<?php echo $user_data['Read_Api'] ?>&results=1", {
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                    },
                })
                   .then(response => response.json())
                   .then(response => 
                   {
                    var string = response["channel"]['description'];
                    array = string.split(",");
                    get_vals(array);
                  });  
                   </script>
     <script>
        var element = document.getElementById("dash");
        element.classList.add("active");

//        fetch('https://api.thingspeak.com/channels/2151406/feeds.json?results=1', {
//     method: 'GET',
//     headers: {
//         'Accept': 'application/json',
//     },
// })
//    .then(response => response.json())
//    .then(response => 
//        document.getElementById("voltage").innerHTML = JSON.stringify(response['feeds']['field1'])
//    )
      </script> 
      <!-- <iframe src="https://thingspeak.com/channels/2151406/field/1.json" frameborder="0" width="90%" height="800"></iframe> -->
    <?php include("footer.php"); ?>
</body>

</html>
