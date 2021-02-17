
$(function() {
    $("#map").googleMap({
      zoom: 5, // Initial zoom level (optional)
      coords: [37.089462, -95.710452], // Map center (optional)
      type: "ROADMAP" // Map type (optional)
    });
  })
 $(function() {
    $("#map2").googleMap();
    $("#map2").addMarker({
      coords: [51.507351, -0.127758], // GPS coords
      title: 'Marker n°1', // Title
      text:  '<b>لورم ایپسوم</b> متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد. کتابهای زیادی در شصت و سه درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد.' // HTML content
    });
  })
  $(function() {
    $("#map3").googleMap();
    
    // Marker 1
    $("#map3").addMarker({
    	 coords: [51.534287, -0.033580]
    });
    
    // Marker 2
    $("#map3").addMarker({
    	 coords: [51.507351, -0.127758]
    });
	
    // Marker 3
    $("#map3").addMarker({
        coords: [37.089462, -95.710452]
    });
  })
    $(function() {
    $("#map4").googleMap();
    $("#map4").addWay({
    	start: "15 avenue des champs Elysées 75008 Paris", // Postal address for the start marker (obligatory)
		end:  [48.895651, 2.290569], // Postal Address or GPS coordinates for the end marker (obligatory)
		route : 'way', // Block's ID for the route display (optional)
		langage : 'english', // language of the route detail (optional)
		step: [ // Array of steps (optional)
		    [48.85837009999999, 2.2944813000000295], // Postal Address or GPS coordinates of the step
		    "Porte Maillot, 75017 Paris", // Postal Address or GPS coordinates of the step
		]
	});
  })
   $(function() {
    $("#map5").googleMap();
    $("#map5").addWay({
    	start: "15 avenue des champs Elysées 75008 Paris", // Postal address for the start marker (obligatory)
		end:  [50.0875726, 14.4189987], // Postal Address or GPS coordinates for the end marker (obligatory)
		route : 'way', // Block's ID for the route display (optional)
		langage : 'english', // language of the route detail (optional)
		step: [ // Array of steps (optional)
		    [48.85837009999999, 2.2944813000000295], // Postal Address or GPS coordinates of the step
		    "Porte Maillot, 75017 Paris", // Postal Address or GPS coordinates of the step
		]
	});
  })
