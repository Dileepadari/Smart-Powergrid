<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title> IOT | Login </title>
  <link rel="stylesheet" href="styles/register.css">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
  <div class="big">
    <div class="container">
      <div class="cover">
        <div class="front">
          <img src="images/aa.jpeg" alt="">
          <div class="text">
            <span class="text-1">A Smart Management of<br> Power Makes You Master</span>
            <span class="text-2">Continue to Your Page</span>
          </div>
        </div>
      </div>
      <div class="forms">
        <div class="form-content">
          <div class="login-form">
            <div class="title">Login</div>
            <form method="POST" action="">
              <div class="input-boxes">
                <div class="input-box">
                  <input type="email" name="email" placeholder="Enter your email" required>
                </div>
                <div class="input-box">
                  <input type="password" name="password" placeholder="Enter your password" required>
                </div>
                <div class="input-box">
                  <input type="radio" id="admin" name="user_type" value="admin" required>
                  <label for="admin" id="admin">Admin</label>
                  <input type="radio" id="user" name="user_type" value="resident" required>
                  <label for="user" id="user">Employee</label>
                </div>
                <br>
                <div class="text"><a href="#" style="color:blue;">Forgot password?</a></div>
                <div class="button input-box">
                  <input type="submit" value="Sumbit">
                </div>
                <br>
                <div class="text sign-up-text">Don't have an account? <a style="color:blue;" href="register.php">Sigup
                    now</a></div>
                <?php
                include("classes/login_c.php");
                    $email = "";
                    $password = "";
                    
                    if($_SERVER['REQUEST_METHOD'] == 'POST')
                    {
                        $login = new Login();
                        $result = $login->evaluate($_POST);
                        if($result != "")
                        {
                          echo "<div style=text-align:center;font-size:18px;color:red;><br>";
                          echo $result;
                        }
                        else{
                          header("Location: index.php");
                          die;
                          
                        }
                        $email = $_POST['email'];
                        $password = $_POST['password'];
                    }
                ?>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</body>

</html>