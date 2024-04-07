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
	  <head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Smart Energy Grid Failure Management System</title>
		<link rel="stylesheet" href="styles/about.css" />
		<link
		  href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap"
		  rel="stylesheet"
		/>
	  </head>
	  <body class="back">

		<br>

        <div class="hero">
            <div class="container">
				<br>
				<div align="middle" style="font-size: 30px; color: aliceblue;">
					<h2 id="typing-effect-h2" style="color: blue;"></h2>
					<p id="typing-effect-p" style="color: blue;"></p>
				  </div>
				  
				  <script>
					const h2Text = "Smart Energy Grid Failure Management System";
				  
					const h2Element = document.getElementById("typing-effect-h2");
					const pElement = document.getElementById("typing-effect-p");
				  
					let h2Index = 0;
					let pIndex = 0;
				  
					function typeH2() {
					  if (h2Index < h2Text.length) {
						h2Element.textContent += h2Text.charAt(h2Index);
						h2Index++;
						setTimeout(typeH2, 40);
					  } else {
						setTimeout(typeP, 100);
					  }
					}
				  
					function typeP() {
					  if (pIndex < pText.length) {
						pElement.textContent += pText.charAt(pIndex);
						pIndex++;
						requestAnimationFrame(typeP);
					  }
					}
				  
					requestAnimationFrame(typeH2);
				  </script>
            </div>
        </div>
	    
	                                            
		<div class="artists">
            <h1 style="font-size: 40px; color:rgb(69, 26, 76)" align="middle">Motivation</h1>
          <br><br>
          <ul class="point-list">
            <li>Energy grids are critical for infrastructure that supplies power to homes, business, and industries.</li>
            <li>However, they are suspectible to various failures , leading to power outages. </li>
            <li>The smart grid represents an opportunity to move the energy industry to a new era of reliability, availability and efficiency by:</li>
            <li>Quick restoration of power after disturbances.</li>
            <li>Reduced operations and management costs.</li>
            <li>Improved security.</li>
            <li>Quick redirection to critical infrastructure for its smooth functioning.</li>
          </ul>
          <br><br>
          
          <h1 style="font-size: 40px; color:rgb(69, 26, 76)" align="middle">How Are We Solving The Problem</h1>
          <br><br>
          <ul class="point-list">
            <li>The project presents an automated and efficient energy grid that can manage various failure scenarios.</li>
            <li>Predictive load assigning based on (manually assigned ) priorities of appliances.</li>
            <li>Addition and removal of devices from the grid and modification of the priorities.</li>
            <li>Redirection of power during grid failures.</li>
            <li>Using temperature sensor for detecting overheating, overloading,etc. in appliances.</li>
            <li>UI for viewing status of the grid ( device health status, total and individual power drawn, etc.) as well as controlling aspects of grid like connecting and disconnecting devices.</li>
            <li>Visualisation and graphs of power consumption over time.</li>
          </ul>
          <br><br>

          <h1 style="font-size: 40px; color:rgb(69, 26, 76)" align="middle">Project Features</h1>
          <br><br>
          <ul class="point-list">
            <li>Using Relays for Switches to control current flow.</li>
            <li>Potentiometers are used to control voltage differences between different preferences in the grid based on data from server.</li>
            <li>Current sensors are used to measure and collect data of current in the circuit.</li>
            <li>DC motors and LEDs are used for appliances in the grid.</li>
            <li>Selecting priorities for load distribution. </li>
            <li>Monitoring and Controlling of grid through remote web server.</li>
            <li>Usage of OM2M for Middleware and ThingSpeak for data collection/Visualization.</li>
            <li>ThingSpeak visualizations of current and health of different appliances in grid over time.</li>
            <li>Control of current trough various parts of grid using information/Alerts given by web server.</li>
          </ul>
          <br><br>1
		</div>	
        <br>

		<div>
			<h1 style="font-size: 50px; color:rgb(69, 26, 76)" align="middle">Meet The Creators</h1>
		</div>

        <br><br>
        <ul class="point-list">
            <li>Faisal</li>
            <li>Samyak Mishra</li>
            <li>Sujal Keshri</li>
            <li>Jayanth</li>
            <li>Ishan Gupta</li>
            <li>Dilip Adari</li>
            <li>Ashish Bharadwaj</li>
            <li>Swaroop</li>
            <li>Karthikeya</li>
            <li>Gadha</li>
            <li>Harshul</li>
        </ul>

		 
		<!-- <div class="artists">
			<div class="container">
		<pre><h1 style="font-size: 35px;"><img  src="../static/sujal2.jpg" alt="Sujal" align="left" style="width: 400px; height: 400px; margin-left: 150px; margin-right: 50px;border-radius: 50%;"><br><br><br><br><br>     Name:  Sujal Keshri<br>     Email: sujal.keshri@students.iiit.ac.in
			</div>
		</div>
        
		<div class="artists">
			<div class="container">
		<pre><h1  style="font-size: 35px;"><img  src="../static/sid1.png" alt="Siddharth" align="right" style="width: 400px; height: 400px; margin-right:220px; border-radius: 50%;"><br><br><br><br><br>        Name:  Siddharth Agarwal<br>        Email: siddharth.agarwal@students.iiit.ac.in<br>
			</div>
		</div> -->

		<br><br><br>
		<!-- <br><br><br>
		<br><br><br> -->
		

 <?php
    include("navbar.php"); 
    ?>

<div class="" style="margin-left: 5%;margin-top: 200px;">


<?php include("footer.php"); ?>
<script>
        var element = document.getElementById("settings");
        element.classList.add("active");
</script>
</div>
