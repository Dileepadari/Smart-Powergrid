
<?php
include("classes/login_c.php");
$login = new Login();
$user_data = $login->check_login($_SESSION['IOT_userid']);
$USER = $user_data;

if(!(isset($USER))){
  
  header("Location: login.php");
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
    <script>
                      function calculatechart(array){
                        var arrayconfig = []
                        array.forEach(element => {
                          
                          console.log(element);
                          document.getElementById("rowe").innerHTML+= `<div class="card "  style="background-color: white;">
            <div class="card-header"> 
              <h2 class="card-title col-11">`+element+`</h2>
            </div>
            <div class="card-body">
              <h3 class="col-12">State : ON</h3>
              <h3 class="speed col-12" id="`+element+`">Speed : 230kmph</h3>
              <h3 class="col-12" id="`+element+`dir">Direction : Clockwise</h3>
              <div class="state" id="`+element+`_state">
                <h3 style="padding: 20px;">Switch State : </h3>
                <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">ON</a>
                <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">OFF</a>
              </div>
              <div class="speed state" id="`+element+`_speed">
              <h3 style="padding: 20px;">Switch speed : </h3>
                <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">Low</a>
                <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">Average</a>
                <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">High</a>
              </div>
              <div class="direction state" id="`+element+`_direction">
              <h3 style="padding: 20px;">Switch direction : </h3>
                <a class="button button-on" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=1">Clockwise</a>
                <a class="button button-off" href="https://api.thingspeak.com/update?api_key=9GI62HJM39P64PLC&field1=0">Anti-CLockwise</a>
              </div>
    
              </div>`;


              if (element.includes("LED") === true || element.includes("Buzzer") === true ) {
                  document.getElementById(element+"_speed").innerHTML = '';
                  document.getElementById(element+"_direction").innerHTML = '';
                  document.getElementById(element).innerHTML = '';
                  document.getElementById(element+"dir").innerHTML = '';

                  }
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
                    calculatechart(array);
                  });  
                   </script>
            
    <!-- <div class="row">
          <div class="col-md-12">
            <div class="card ">
              <div class="card-header ">
                <h5 class="card-title">Voltage Behaviour</h5>
                <p class="card-category">24 Hours performance</p>
              </div>
              <div class="card-body ">
                <canvas id=chartHours width="400" height="100"></canvas>  
              </div>
              <div class="card-footer ">
                <hr>
                <div class="stats">
                  <i class="fa fa-history"></i> Updated 3 minutes ago
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="card ">
              <div class="card-header ">
                <h5 class="card-title">Health&nbsp;Analysis</h5>
                <p class="card-category">Last&nbsp;Month&nbsp;Performance</p>
              </div>
              <div class="card-body ">
                <canvas id="chartEmail" height="195"></canvas>
              </div>
              <div class="card-footer ">
                <div class="legend">
                  <i class="fa fa-circle text-primary"></i> Healthy
                  <i class="fa fa-circle text-warning"></i> Read
                  <i class="fa fa-circle text-danger"></i> Danger
                  <i class="fa fa-circle text-gray"></i> Stopped
                </div>
                <hr>
                <div class="stats">
                  <i class="fa fa-calendar"></i> Number of Readings : 200
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-8">
            <div class="card card-chart">
              <div class="card-header">
                <h5 class="card-title">Humidity&nbsp;And&nbsp;Temperature</h5>
                <p class="card-category">Analysis over Month</p>
              </div>
              <div class="card-body">
              <iframe width="100%" height="240" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/2151406/charts/1?api_key=KB9Q1GLXUP2ZFT7N&width=auto&color=00FFFF"></iframe>
              <canvas id="speedChart" width="400" height="100"></canvas>
              </div>
              <div class="card-footer">
                <div class="chart-legend">
                  <i class="fa fa-circle text-info"></i> Humidity
                  <i class="fa fa-circle text-warning"></i> Temperature
                </div>
                <hr/>
                <div class="card-stats">
                  <i class="fa fa-check"></i> Data information certified
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>-->
      <script>
        var element = document.getElementById("dash");
        element.classList.add("active");
        fetch('https://api.thingspeak.com/channels/2151406/feeds.json?results=1', {
    method: 'GET',
    headers: {
        'Accept': 'application/json',
    },
})
   .then(response => response.json())
   .then(response => 
       document.getElementById("voltage").innerHTML = JSON.stringify(response['feeds']['field1'])
   )
      </script>
      <!-- <iframe src="https://thingspeak.com/channels/2151406/field/1.json" frameborder="0" width="90%" height="800"></iframe> -->
    <?php include("footer.php"); ?>
</body>

</html>
