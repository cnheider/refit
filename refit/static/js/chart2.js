function Chart(error, dataJson, IcontainerId) {
  // Private variables
  // Declarations
  var containerId;
  var container;
  var chart;
  var margin = {
    top: 20,
    right: 80,
    bottom: 30,
    left: 50
  }
  var width = 1000,
    height = 400;
  var x, x_axis;
  var y;
  var y_left, y_axis_left;
  var y_right, y_axis_right;
  var color = d3.scaleOrdinal(d3.schemeCategory10);
  var int_line = d3.line()
    .x(function (d) {
      return x(extract_date(d));
    })
    .y(function (d) {
      return y(extract_int_val(d));
    });

  // Initialisations
  var _init = function () {
    containerId = IcontainerId;
    container = d3.select("#" + containerId);

    update_dimensions_derived_from_container();
    append_svg_child();
    x_axis_reinit();
    y_axis_reinit();
    append_x_axis();
    append_y_axis();
    append_lines();
    append_points();

  }
  var x_axis_reinit = function () {
    x = d3.scaleTime()
      .range([0, width]);

    x.domain(d3.extent(dataJson, extract_date));

    x_axis = d3.axisBottom()
      .scale(x)
  }
  var y_axis_reinit = function () {
    y = d3.scaleLinear()
      .range([height, 0]);

    y.domain(d3.extent(dataJson, extract_int_val));

    y_axis = d3.axisLeft()
      .scale(y)
  }

  // Event handlers
  var update_dimensions_derived_from_container = function () {
    containerElement = document.getElementById(containerId);
    width = parseInt(window.getComputedStyle(containerElement).getPropertyValue('width')) - (margin.right + margin.left); // width
    height = parseInt(window.getComputedStyle(containerElement).getPropertyValue('height')) - (margin.top + margin.bottom); // height
  }
  var handle_window_resize_event = function () {
    update_dimensions_derived_from_container()

    // reset width/height of SVG
    d3.select("#" + containerId + " svg")
      .attr("width", width + margin.right + margin.left)
      .attr("height", height + margin.top + margin.bottom);
  }

  // Appends
  var append_svg_child = function () {
    chart = container.append("svg:svg")
      .attr("class", "line-chart")
      .attr("width", width + margin.right + margin.left)
      .attr("height", height + margin.top + margin.bottom)
      .append("svg:g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  }
  var append_x_axis = function () {
    chart.append("svg:g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(x_axis)
      .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Date");
  }
  var append_y_axis = function () {
    chart.append("svg:g")
      .attr("class", "y axis")
      //.attr("transform", "translate(50,0)")
      .call(y_axis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Steps");
  }
  var append_lines = function () {
    chart.append("path")
      .datum(dataJson)
      .attr("class", "line")
      .attr("id", function (d) {
        return "line" + extract_data_type_name(d);
      })
      .attr("d", int_line)
      .style("stroke", function (d) {
        return color(extract_data_type_name(d));
      });
  }

  var append_points = function () {
    int_tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
      return extract_int_val(d);
    });

    points = chart.selectAll(".point")
      .data(dataJson)
      .enter().append("circle")
      .attr("class", "point")
      .attr("clip-path", "url(#clip)")
      .attr("r", function (d) {
        return 3;
      })
      .attr("cx", function (d) {
        return x(extract_date(d));
      })
      .attr("cy", function (d) {
        return y(extract_int_val(d));
      })
      .call(int_tip).on('mouseover', int_tip.show)
      .on('mouseout', int_tip.hide);
  }

  // Helper functions
  function extract_date(d) {
    return new Date(d['endTimeNanos'] / 1000 / 1000);
  }

  function extract_int_val(d) { //Integer value
    return d['value'][0]['intVal'];
  }

  function extract_data_type_name(d) {
    return d[0]['dataTypeName'];
  }

  // Execute
  _init();
};
