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
    <div id="healthDataContainer">
               
            <div class="healthData" id="healthData" style="height: 370px; width: 70%;"></div>
            <script type="text/javascript">
                function calculatechart(array){
                    var arrayconfig = [];
                    var colors = ["green", "orange", "red"];
                    array.forEach(element => {
                        var z = Math.floor(Math.random(1000) * (4 - 1) + 1);
                        arrayconfig.push({ y : z, label :element, color: colors[z-1]});
                    });
                    displaychart(arrayconfig)
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
                                           labelFontColor: "dimGrey"
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

            </script>';
    </div>


<?php include("footer.php"); ?>
</div>
<!-- <div id="chartContainer" style="height: 370px; width: 100%;"></div> -->
<script>
        var element = document.getElementById("health");
        element.classList.add("active");
</script>
