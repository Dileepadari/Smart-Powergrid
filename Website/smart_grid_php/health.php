<?php
include("classes/login_c.php");
if(!(isset($_SESSION['IOT_userid']))){
    header("Location: login.php");
    die;
}
$login = new Login();
$user_data = $login->check_login($_SESSION['IOT_userid']);
// print_r($user_data);
// print_r($user_data);
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
<head>
    <link rel="stylesheet" type="text/css" href="styles/health.css">
    <script src="https://cdn.canvasjs.com/canvasjs.min.js"></script>
</head>
<div class="main-panel">
    <?php include("navbar.php"); ?>
    <h1 style="margin-top: 100px;margin-left: 100px;text-align: left;">Health Data</h1>
    <div id="healthDataContainer" style = "min-height: 78vh;">
<div style="margin-left: 30vw;font-size: 22px;">Labels:</div>
        <div style="display: flex;margin-left: 40vw;font-size: 22px;">  Y-axis:   <div style=""><i style="color: red;">1. Bad condition</i><br><i style="color: orange;">2. Average condition</i><br><i style="color: green;">3. Good condition</i></div></div>
        <div style="display: flex;margin-left: 48vw;font-size: 22px;">X-axis:  Appliances</div><br><br>
            <div class="healthData" id="healthData" style="height: 370px; width: 70%;"></div>
            <script type="text/javascript">
                function calculatechart(array){
                    var arrayconfig = [];
                    var colors = ["red", "orange", "green"];
                    <?php $hi = $user_data['field_no']+1; ?>
                    fetch("https://api.thingspeak.com/channels/<?php echo $user_data['channel_id'] ?>/fields/<?php echo $hi ?>.json?api_key=<?php echo $user_data['Read_Api'] ?>&results=1", {
                    method: "GET",
                    headers: {
                        "Accept": "application/json",
                    },
                })
                   .then(response => response.json())
                   .then(response => 
                   {
                var string = response["feeds"][0]["field<?php echo $hi ?>"];
                values = string.split(",");
                i = 0;
                array.forEach(element => {
                    element = element.replace("&#39;", "").replace("&#39;", "");
                    var z = Math.floor(Math.random(1000) * (4 - 1) + 1);
                    arrayconfig.push({ y: parseInt(values[i]), label: element, color: colors[parseInt(values[i]) - 1] });
                    i = i+1;
                });
                displaychart(arrayconfig);
            });
            }
                function displaychart(array)
               {
                console.log(array);
                       var chart = new CanvasJS.Chart("healthData", {
                               title: {
                                       text: "Health Analysis"
                                   },
                                   axisY: {
                                           labelFontSize: 20,
                                           labelFontColor: "dimGrey",
                                           minimum: 0,
                                           maximum: 3
                        },
                        data: [
                            {
                                    type: "column",
                                    dataPoints: array
                                    }
                                    ]
                                });
                            
                            chart.render();
                        }
                var array = [];
                
                fetch("https://api.thingspeak.com/channels/<?php echo explode(",",$user_data['channel_id'])[0] ?>/fields/1.json?api_key=<?php echo explode(",",$user_data['Read_Api'])[0] ?>&results=1", {
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
    </div>


<?php include("footer.php"); ?>
</div>
<!-- <div id="chartContainer" style="height: 370px; width: 100%;"></div> -->
<script>
        var element = document.getElementById("health");
        element.classList.add("active");
</script>
