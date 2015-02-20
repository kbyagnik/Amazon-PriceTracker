<html>

<head>
<title>AWS | 2015
</title>
<style>
  /**************************CSS************************/
  #wrapper {
  	margin: 20px;
  	min-height: 500px;
  }
  #search {
  	font-size: 16px;
  	background: #f5f5f5;
  	margin: -20px;
  	padding: 20px;
  	padding-bottom: 5px;
  	margin-bottom: 10px;
  }
  #header {
  	height: 100px;
  	background: #f5a5a5;
  	margin-top: -20px;
  }
  #header h1{
  	padding-top: 30px;
  	padding-left: 20px;
  	font-variant: small-caps;
  	font-size: 50px;
  	color: white;
  }
	h2 {
		color: #ccc !important;
	}
	#desc {
		font-size: 14px;
	}
	#query {
		width: 400px;
	}
	input[type="text"] {
  padding: 12px;
  border: solid 1px #dcdcdc;
  transition: box-shadow 0.3s, border 0.3s;
}
input[type="text"]:focus,
input[type="text"].focus {
  border: solid 1px #707070;
  box-shadow: 0 0 5px 1px #969696;
}
input[type="submit"] {
	padding: 3px 24px;
	color: white;
	background: #f57575;
	box-shadow: none;
	border: none;
}
input[type="submit"]:hover {
	
	background: #c51515;
}
#footer {
	padding: 10px;
	padding-left: 20px;
	background: #333;
	/*position: fixed;*/
	bottom: 0;
	width: 100%;
	color: white;
}
</style>
<link rel="stylesheet" href="/bootstrap.min.css">
<script type="text/javascript" src="/canvasjs.min.js"></script>
 <script type="text/javascript">
 var datetimeToDate = function(datetime_str, use_utc) {
  // Return a JS Date object from the given python datetime_str string.
  // if the optional boolean use_utc argument is given, the datetime_str
  // will be treated as a UTC datetime_str
  "use strict";
  var datetime_parts = datetime_str.split(" ", 2),
    date_parts = datetime_parts[0].split("-"),
    time_parts = datetime_parts[1].split(":"),
    second_parts = time_parts[2].split('.'),
    mkdate,
    s2i,
    smu2ims;
  use_utc = use_utc === undefined ? false : use_utc;

  // The Date constructors don't work with .apply(), so lambdas
  if (use_utc) {
    mkdate = function (y, m, d, hr, min, sec, ms) {
      return new Date(Date.UTC(y, m, d, hr, min, sec, ms));
    };
  } else {
    mkdate = function (y, m, d, hr, min, sec, ms) {
      return new Date(y, m, d, hr, min, sec, ms);
    };
  }

  // string to int with radix 10
  s2i = function (i_str) { return parseInt(i_str, 10); };

  // string microsecond (aka mu) to int millisecond (aka ms)
  smu2ims = function (f_str) {
    return Math.round(parseFloat(f_str) * 1000);
  };

  return mkdate(s2i(date_parts[0]), // year
                s2i(date_parts[1]) - 1, // month 
                s2i(date_parts[2]), // day
                s2i(time_parts[0]), // hour
                s2i(time_parts[1]), // minute
                s2i(second_parts[0]), // second
                smu2ims("." + second_parts[1])); // millisecond
}

  window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {
      theme: "theme2",
      title:{
        text: "Price History"
      },
      animationEnabled: true,
      axisX: {
        valueFormatString: "h:mm tt, D MMM YYYY",
        interval:1,
        intervalType: "month"
        
      },
      axisY:{
        includeZero: false
        
      },
      data: [
      {        
        type: "line",
        //lineThickness: 3,        
        dataPoints: [
        <?php
	if (isset($_GET['pid'])) {
  		$pid = $_GET['pid'];
  		$m = array();
  		preg_match("/[A-Z]([A-Z0-9]{9})/",$pid,$m);
  		$pid = $m[0];

	try {
	    $db_url = "mongodb://localhost:27017" ;
	    $connect = new MongoClient($db_url);
	    $db_name = "amazon" ;
	    $db = $connect->selectDB($db_name);
	    $collection = $db->selectCollection("products");
	    $data = $collection->findOne(array("pid" => $pid));
	    if(isset($data)) {
	    $size = sizeof($data['price']);
	    // echo $size;
	    for ($x = 0; $x < $size; $x++) {
	    	echo "{ x: datetimeToDate(\"" . $data['timestamp'][$x] . "\"), y: " . str_replace(",","",$data['price'][$x]) . "}," . "\n";
	    }}
	    // disconnect from server
	    $connect->close();
	  } catch ( MongoConnectionException $e ) {
	    die('Cannot connect to MongoDB server');
	  } catch ( MongoException $e ) {
	    die('Mongo Error: ' . $e->getMessage());
	  } catch ( Exception $e ) {
	    die('Error: ' . $e->getMessage());
	  }
	}
?>
        ]
      }
      
      
      ]
    });

chart.render();
} 
</script> 
</head>

<body>
	<div id='header'>
	<h1>Amazon Web Scrapers (AWS)</h1>
</div>
	<div id="wrapper">
	<div id='search'>
	<center><form action='#' method=GET>
		Enter Product URL: &nbsp;<input name=pid id='query'>
		&nbsp;<input type=submit value=Search>
	</form></center>
</div>
	<?php if(isset($data)) {
	echo "<h2> Product Description #" . $pid . "</h2><div id='desc'>";
	echo "Name: " . $data['name'];
	echo "<br> Rating: " . $data['rating'];
	echo "<br> Latest Price: Rs " . $data['price'][$size - 1];
	echo "<br> Number of Reviews: " . $data['reviews'];
	echo "<br>Description<ul>";
	foreach($data['desc'] as $desc) {
		echo "<li>" . $desc . "</li>";
	}
	echo "</ul><a target=_blank href=" . $data['url'] . ">View this product on Amazon</a></div>";
 	echo "<div id='chartContainer' style='height: 300px; width: 100%;''></div>";
	}
	?>
</div>
<div id="footer">
Powered by Aragog &nbsp; | &nbsp; 2015
</div>
</body>


</html>
