<!DOCTYPE html>
<html lang="en">

<?php include("header.php");  ?>
    <div class="main-panel">
      <!-- Navbar -->
      <?php include("navbar.php");  ?>
      <div class="content">
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
                      <p class="card-title">150mv
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
                      <i class="nc-icon nc-atom text-warning"></i>
                    </div>
                  </div>
                  <div class="col-7 col-md-8">
                    <div class="numbers">
                      <p class="card-category">Temperature</p>
                      <p class="card-title"><span id="temperature">25</span>&nbsp;deg&nbsp;C
                        <p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-footer ">
                <hr>
                <div class="stats">
                  <i class="fa fa-calendar-o"></i> Last day
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
                      <p class="card-category">Humidity</p>
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
        <div class="row">
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
                <!--<canvas id="speedChart" width="400" height="100"></canvas>-->
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
      </div>
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
   
      document.getElementById("temperature").innerHTML = JSON.stringify(response['feeds'][0]['field1']).replace(/"/g, ""))
      </script>
      <!-- <iframe src="https://thingspeak.com/channels/2151406/field/1.json" frameborder="0" width="90%" height="800"></iframe> -->
      <!-- <iframe src="https://fortress.maptive.com/ver4/475ddcbab1805685015d6571eb9d778d/573815" frameborder="0" width="90%" height="800" style="margin-left:5%" allow="geolocation"></iframe> -->
    <?php include("footer.php"); ?>
</body>

</html>
