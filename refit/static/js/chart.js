function Chart(error, stepsJson, hrJson, sleepJson, weightJson, cal_burned_json, IcontainerId) {
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
      return y_left(extract_int_val(d));
    });
  var fp_line = d3.line()
    .x(function (d) {
      return x(extract_date(d));
    })
    .y(function (d) {
      return y_right(extract_fp_val(d));
    });

  // Initialisations
  var _init = function () {
    containerId = IcontainerId;
    container = d3.select("#" + containerId);

    update_dimensions_derived_from_container();
    append_svg_child();
    x_axis_reinit();
    y_axis_left_reinit();
    y_axis_right_reinit();
    append_x_axis();
    append_y_axis_left();
    append_y_axis_right();
    append_lines();
    append_legend();
    append_points();
    /*
        var brush = d3.brush()
          .x(x)
          .on("brush", brushmove)
          .on("brushend", brushend);

        chart.append("g")
          .attr("class", "brush")
          .call(brush)
          .selectAll('rect')
          .attr('height', height);

        function brushmove() {
          var extent = brush.extent();
          points.classed("selected", function (d) {
            is_brushed = extent[0] <= d.index && d.index <= extent[1];
            return is_brushed;
          });
        }

        function brushend() {
          get_button = d3.select(".clear-button");
          if (get_button.empty() === true) {
            clear_button = svg.append('text')
              .attr("y", 460)
              .attr("x", 825)
              .attr("class", "clear-button")
              .text("Clear Brush");
          }

          x.domain(brush.extent());

          transition_data();
          reset_axis();

          points.classed("selected", false);
          d3.select(".brush").call(brush.clear());

          clear_button.on('click', function () {
            x.domain([0, 50]);
            transition_data();
            reset_axis();
            clear_button.remove();
          });
        }

        function transition_data() {
          svg.selectAll(".point")
            .data(stepsJson)
            .transition()
            .duration(500)
            .attr("cx", function (d) {
              return x(d.index);
            });
        }

        function reset_axis() {
          svg.transition().duration(500)
            .select(".x.axis")
            .call(x_axis);
        }*/

  }
  var x_axis_reinit = function () {
    x = d3.scaleTime()
      .range([0, width]);

    x.domain(d3.extent(hrJson, extract_date));

    x_axis = d3.axisBottom()
      .scale(x)
  }
  var y_axis_left_reinit = function () {
    y_left = d3.scaleLinear()
      .range([height, 0]);

    y_left.domain(d3.extent(stepsJson, extract_int_val));

    y_axis_left = d3.axisLeft()
      .scale(y_left)
  }
  var y_axis_right_reinit = function () {
    y_right = d3.scaleLinear()
      .range([height, 0]);

    y_right.domain(d3.extent(hrJson, extract_fp_val));

    y_axis_right = d3.axisRight()
      .scale(y_right)
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
  var append_y_axis_left = function () {
    chart.append("svg:g")
      .attr("class", "y axis")
      //.attr("transform", "translate(50,0)")
      .call(y_axis_left)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Steps");
  }
  var append_y_axis_right = function () {
    chart.append("svg:g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + width + ",0)")
      .call(y_axis_right)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -12)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("HR");
  }
  var append_lines = function () {
    chart.append("path")
      .datum(stepsJson)
      .attr("class", "line")
      .attr("d", int_line)
      .style("stroke", function (d) {
        return color(extract_data_type_name(d));
      });

    /*chart.append("path")
      .datum(sleepJson)
      .attr("class", "line")
      .attr("d", int_line)
      .style("stroke", function (d) {
        return color(extract_data_type_name(d));
      });*/

    /*chart.append("path")
      .datum(weightJson)
      .attr("class", "line")
      .attr("d", fp_line)
      .style("stroke", function (d) {
        return color(extract_data_type_name(d));
      });*/

    chart.append("path")
      .datum(hrJson)
      .attr("class", "line")
      .attr("d", fp_line)
      .style("stroke", function (d) {
        return color(extract_data_type_name(d));
      });
    /*
        chart.append("path")
          .datum(cal_burned_json)
          .attr("class", "line")
          .attr("d", fp_line)
          .style("stroke", function (d) {
            return color(extract_data_type_name(d));
          });*/
  }
  var append_legend = function () {
    var legend = chart.selectAll(".legend")
      .data(color.domain())
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function (d, i) {
        return "translate(0," + i * 20 + ")";
      });

    legend.append("rect")
      .attr("x", width - 18 - 20)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

    legend.append("text")
      .attr("x", width - 24 - 20)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function (d) {
        return d;
      });
  }
  var append_points = function () {
    tip = d3.tip().attr('class', 'd3-tip').html(function (d) {
      return extract_int_val(d);
    });

    points = chart.selectAll(".point")
      .data(stepsJson)
      .enter().append("circle")
      .attr("class", "point")
      .attr("clip-path", "url(#clip)")
      .attr("r", function (d) {
        return 5;
      })
      .attr("cx", function (d) {
        return x(extract_date(d));
      })
      .attr("cy", function (d) {
        return y_left(extract_int_val(d));
      })
      .call(tip).on('mouseover', tip.show)
      .on('mouseout', tip.hide);
  }

  // Helper functions
  function extract_date(d) {
    return new Date(d['endTimeNanos'] / 1000 / 1000);
  }

  function extract_int_val(d) { //Integer value
    return d['value'][0]['intVal'];
  }

  function extract_fp_val(d) { //Floating point value
    return d['value'][0]['fpVal'];
  }

  function extract_data_type_name(d) {
    return d[0]['dataTypeName'];
  }

  // Execute
  _init();
};
