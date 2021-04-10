// Main js for the frontend of "web-contact-converter"
// Collin Sparks, Feb 2021
// cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

function replace_brs(with_tags) { // a contenteditable div uses <br> tags instead of \n, so we need to replace those
  const regex = /<br>/;
  let no_tags = with_tags.replace(regex, '\n');
  return no_tags;
};


function send_request(destination) {
  if (destination === 'py_compile') { // only takes data from textarea if called from compile button
    let target = document.getElementById('textarea');
    var sendthis = {
      message: replace_brs(target.value)
    }
  } else {
    var sendthis = {
      message: 'dummy-value'
    }
  }
  set_checkboxes({nodes_list: undefined, toggle: undefined, checked: false}) // unchecks all checkboxes. we will check all of the new ones later.

  fetch(`${window.origin}/${destination}`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(sendthis),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function(response) { // receives the response
    if (response.status !== 200) {
      console.log(`There was an error! Code ${response.status}`);
      return ;
    }
    return response.json()
  })
  .then(function(data) { // builds table elements from the data in response
    let table = document.getElementById('select-form')

    for (let company of data) { // creates table rows and appends them to the table
      let tmp = create_row(company) // separated from next line so that we can still access the elemnent in the line after
      table.appendChild(tmp)
      console.log('appending')
      tmp.querySelector("[type='checkbox']").checked = true
    }
    return document.querySelectorAll('.table-row').length -1 // the -1 accounts for the table header row
  })
  .then(function(length) { // this will update the COMPANIES IN SESSION banner
    console.log('in banner update')
    let elem = document.querySelector('#session-counter')
    elem.textContent = `Companies: ${length}`
  })
};


function setAttributes(element, dict_of_attrs) { // adding multiple attrs at once to an element; takes a dict
  for(var key in dict_of_attrs) {
    element.setAttribute(key, dict_of_attrs[key])
  }
};


function create_row(company) { // one company's worth of information
  let newDiv = document.createElement('div')
  newDiv.classList.add('table-row')

  let field_types = [ // in the order that they appear left-to-right on the page
    'name',
    'contacts',
    'emails',
    'phones',
    'address',
  ]
  newDiv.appendChild(create_fields('select', company.emails[0])) // first piece of the row from left-to-right
  for (const type of field_types) {
    newDiv.appendChild(create_fields(type, company[type])) //
  }
  newDiv.appendChild(create_fields('spacer')) //used for spacing on the page, empty div in the column of the delete-selected button
  return newDiv; // this should be a complete row
};


function create_fields(type, data='') { // takes a dict of contact data and makes them into table fields/cells
  if (type === 'select') { // contains the select checkbox
    let selectField = document.createElement('div')
    selectField.classList.add('table-field', 'checkbox')

    let selectBox = document.createElement('input') // the actual <input type='checkbox'>
    setAttributes(selectBox, {'type': 'checkbox', 'name': data})
    selectField.appendChild(selectBox)
    return selectField;

  } else if (type === 'spacer') { // used for spacing on the page, empty div in the column of the delete-selected button
    let spacerField = document.createElement('div')
    spacerField.classList.add(['table-field'])
    return spacerField;

  } else { // uses the data to label and fill the table cell
    let field = document.createElement('div')
    field.classList.add(['table-field'])
    field.setAttribute('name', type)
    field.textContent = data
    return field;
  }
};


function set_checkboxes(params) {
  // node_list: (array) if no list of nodes passed, then function selects all nodes on the document.
  // toggle = (bool) optionally toggle checked/unchecked
  // checked = (bool) set all nodes to checked(true) or unchecked(false)

  if (typeof(params.node_list) === typeof(['array'])) {
    var nodes = params.node_list
  } else {
    var nodes = document.querySelectorAll("input[type='checkbox']")
  }

  if (params.toggle) {
    let i = 0
    for (let node of nodes) {
      if (node.checked === false) { // if any node is unchecked, then i > 0
        i = i + 1
      }
    }

    if (i === 0) { // all nodes are checked
      for (let node of nodes) {
        node.checked = false // uncheck them all
      }
    } else { // if at least one node is unchecked
      for (let node of nodes) {
        node.checked = true // check them all
      }
    }
  }

  if (!(params.checked === undefined)) { // if an argument was passed (bool)
    for (let node of nodes) {
      node.checked = params.checked // true or false!
    }
  }

};


function select_toggle() { // lazy solution to select-all button's onclick
  set_checkboxes({node_list: false, toggle: true, checked: undefined})
};


function generate() {
  fetch(`${window.origin}/py_generate`, { // sending the request
    method: "POST",
    credentials: "include",
    // body:
    cache: "no-cache",
    headers: new Headers({
      "content-type": "text/plain"
    })
  })
  .then(response => response.blob())
  .then(blob => URL.createObjectURL(blob))
  .then(url => {
    window.open(url, '_blank')
    URL.revokeObjectURL(url)
  })
}


window.onload = (event) => { // appends existing data to table on page load
  send_request('compile_from_session')
}

var compileElement = document.querySelector('#compile-button') // adds listener for compile button
compileElement.addEventListener('click', function() {
  send_request('py_compile')
})
