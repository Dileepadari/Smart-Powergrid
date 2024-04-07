<?php
include("database_c.php");
class Signup
{
    private $error = "";

    public function evaluate($data)
    {

        foreach ($data as $key => $value) {
            # code...

            if(empty($value))
            {
                $this->error = $this->error . $key . " is empty!<br>";
            }

            if($key == "email")
            {
                if (!preg_match("/([\w\-]+\@[\w\-]+\.[\w\-]+)+\.[\w\-]+)/",$value)) {
        
                        $this->error = $this->error . "invalid email address!<br>";
                }
            }

            if($key == "fullname")
            {
                if (is_numeric($value)) {
        
                        $this->error = $this->error . "name cant be a number<br>";
                }

            }

        
            
        }

        $DB = new Database();

        

        $data['userid'] = $this->create_userid();
        //check userid
        $sql = "select userid from Users where userid = '$data[userid]' limit 1";
        $check = $DB->read($sql);
        while(is_array($check)){

            $data['userid'] = $this->create_userid();
            $sql = "select userid from Users where userid = '$data[userid]' limit 1";
            $check = $DB->read($sql);
        }

        //check email
        $sql = "select userid from Users where email = '$data[email]' limit 1";
        $check = $DB->read($sql);
        if(is_array($check)){

                $this->error = $this->error . "Another user is already using that email<br>";
        }
    

        if($this->error == "")
        {
    
            //no error
            $this->create_user($data);
        
        }else
        {
            return $this->error;
        }
    }

    public function create_user($data)
    {

        $username = ucfirst($data['username']);
        $email = $data['email'];
        $password = $data['password'];
        $userid = $data['userid'];
        $date = date("Y-m-d H:i:s");
        $user_type = "user";

        $password = hash("sha1", $password);
        
        //create these
        

        $query = "insert into Users 
        (user_type,userid,username,email,password,date) 
        values 
        ('$user_type','$userid','$username','$email','$password','$date')";


        $DB = new Database();
        $DB->save($query);
    }
    
    private function create_userid()
    {

        $length = rand(4,19);
        $number = "";
        for ($i=0; $i < $length; $i++) { 
            # code...
            $new_rand = rand(0,9);

            $number = $number . $new_rand;
        }

        return $number;
    }
}

?>