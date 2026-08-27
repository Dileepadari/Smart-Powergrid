<?php
include("classes/login_c.php");

$admin_login = new login();
$user_data = $admin_login->check_admin_login($_SESSION['IOT_userid']);

$USER = $user_data;
if(!(isset($USER))){
  
  header("Location: login.php");
}
$userid = $user_data['userid'];
$db = new Database();
$query = "select * from Users where userid != '$userid' AND user_type = 'resident' ";
$admin_data = $db->read($query);

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
        <div class="row">
          <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
              <div class="card-body ">
                <div class="row">
                  <div class="col-5 col-md-4">
                    <div class="icon-big text-center icon-warning">
                      <i class="nc-icon nc-bulb-63 text-danger"></i>
                    </div>
                  </div>
                  <div class="col-7 col-md-8">
                    <div class="numbers">
                      <p class="card-category">Voltage</p>
                      <p class="card-title"  id="voltage">150mv
                        <p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer ">
                <hr>
                <div class="stats">
                  <i class="fa fa-refresh"></i>Update
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
              <div class="card-body ">
                <div class="row">
                  <div class="col-5 col-md-4">
                    <div class="icon-big text-center icon-warning">
                      <i class="nc-icon nc-vector text-success"></i>
                    </div>
                  </div>
                  <div class="col-7 col-md-8">
                    <div class="numbers">
                      <p class="card-category">Current</p>
                      <p class="card-title">23
                        <p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer ">
                <hr>
                <div class="stats">
                  <i class="fa fa-clock-o"></i> In the last hour
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6 col-sm-6">
            <div class="card card-stats">
              <div class="card-body ">
                <div class="row">
                  <div class="col-5 col-md-4">
                    <div class="icon-big text-center icon-warning">
                      <i class="nc-icon nc-favourite-28 text-primary"></i>
                    </div>
                  </div>
                  <div class="col-7 col-md-8">
                    <div class="numbers">
                      <p class="card-category">System&nbsp;Health</p>
                      <p class="card-title">60%
                        <p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer ">
                <hr>
                <div class="stats">
                  <i class="fa fa-send"></i> Health Analysis
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row" >
        <div class="col-md-12" id="rowe">
          <br>
          <h3>User Controls</h3>
          
        </div>
      </div>
    </div>
    <?php

    foreach ($admin_data as $key => $user) {
        $name = $user['username'];
        echo '<script>
        function calculatechart(array,name){
                      var arrayconfig = []
                      array.forEach(element => {
                        
                        console.log(element);
                        document.getElementById("rowe").innerHTML+= `<div class="card "  style="background-color: white;">
                        <div class="card-header"> 
                        <h2 class="card-title col-11">`+element+` ( `+name+` )</h2>
                        </div>
                        <div class="card-body">
                        <h3 class="col-12">State : ON</h3>
                        <h3 class="speed col-12" id="`+element+`">Speed : 230kmph</h3>
                        <h3 class="col-12" id="`+element+`dir">Direction : Clockwise</h3>`;
                        if (element.includes("LED") === true || element.includes("Buzzer") === true ){
                                document.getElementById(element+"dir").innerHTML = "";
                                document.getElementById(element).innerHTML = "";
                                }
                    });

                    }
                        
              var array = [];
      fetch("https://api.thingspeak.com/channels/'.$user["channel_id"].'/fields/1.json?api_key='.$user["Read_Api"].'&results=1", {
      method: "GET",
      headers: {
          "Accept": "application/json",
      },
  })
     .then(response => response.json())
     .then(response => 
     {
      var string = response["channel"]["description"];
      var name = response["channel"]["name"];
      array = string.split(",");
      calculatechart(array, name);

     });  
      
        </script>';
        // die;
//         echo '<script>
//         function calculatechart(array){
//           var arrayconfig = []
//           array.forEach(element => {
            
//             console.log(element);
//             document.getElementById("rowe").innerHTML+= `<div class="card "  style="background-color: white;">
// <div class="card-header"> 
// <h2 class="card-title col-11">`+element+`</h2>
// </div>
// <div class="card-body">
// <h3 class="col-12">State : ON</h3>
// <h3 class="speed col-12" id="`+element+`">Speed : 230kmph</h3>
// <h3 class="col-12" id="`+element+`dir">Direction : Clockwise</h3>
// <div class="state" id="`+element+`_state">
//   <h3 style="padding: 20px;">Switch State : </h3>
//   <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">ON</a>
//   <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">OFF</a>
// </div>
// <div class="speed state" id="`+element+`_speed">
// <h3 style="padding: 20px;">Switch speed : </h3>
//   <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">Low</a>
//   <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">Average</a>
//   <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">High</a>
// </div>
// <div class="direction state" id="`+element+`_direction">
// <h3 style="padding: 20px;">Switch direction : </h3>
//   <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">Clockwise</a>
//   <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">Anti-CLockwise</a>
// </div>

// </div>`;


// if (element.includes("LED") === true || element.includes("Buzzer") === true ) {
//     document.getElementById(element+"_speed").innerHTML = '';
//     document.getElementById(element+"_direction").innerHTML = '';
//     document.getElementById(element).innerHTML = '';
//     document.getElementById(element+"dir").innerHTML = '';

//     }
// });
//         }
//  echo '<script>
//       var array = [];
//       fetch("https://api.thingspeak.com/channels/'.$user["channel_id"].'/fields/1.json?api_key='.$user["Read_Api"].'&results=1", {
//       method: "GET",
//       headers: {
//           "Accept": "application/json",
//       },
//   })
//      .then(response => response.json())
//      .then(response => 
//      {
//       var string = response["channel"]["description"];
//       array = string.split(",");
//     //   calculatechart(array);
//     });  
//      </script>'
    }?>
   
    
      <script>

        var element = document.getElementById("dash");
        element.classList.add("active");

//         fetch('https://api.thingspeak.com/channels/2151406/feeds.json?results=1', {
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
