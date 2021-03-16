// Main js for the frontend of "web-contact-converter"
// Collin Sparks, Feb 2021

function replace_brs(with_tags) { // a contenteditable div uses <br> tags instead of \n, so we need to replace those
  const regex = /<br>/;
  let no_tags = with_tags.replace(regex, '\n');
  return no_tags;
};


function send_request(destination) {
  if (destination === 'py_compile') { // only takes from textarea if called from button
    let target = document.getElementById('textarea');
    // console.log(target.value);
    var sendthis = {
      message: replace_brs(target.value)
    }
  } else {
    var sendthis = {
      message: 'dummy-value'
    }
  }
  set_checkboxes({nodes_list: undefined, toggle: undefined, checked: false}) // unchecks all checkboxes. we will check all of the new ones.

  // console.log(destination)
  fetch(`${window.origin}/${destination}`, { // sending the request
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
    response.json().then(function(data) { // processes the
      // console.log(`data: ${data}`)
      let table = document.getElementById('companies-wrapper')

      for (let company of data) { // creates table rows and appends them to the table
        // console.log(`company: ${company.name}`)
        let tmp = create_row(company) // separated from next line so that we can still access the elemnent in the line after
        table.appendChild(tmp)
        tmp.querySelector("[type='checkbox']").checked = true
      }
    })
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

  field_types = [ // in the order that they appear left-to-right on the page
    'name',
    'contacts',
    'emails',
    'phones',
    'address',
  ]
  newDiv.appendChild(create_fields('select')) // first piece of the row from left-to-right
  for (const type of field_types) {
    newDiv.appendChild(create_fields(type, company[type]))
  }
  newDiv.appendChild(create_fields('spacer')) //used for spacing on the page, empty div in the column of the delete-selected button
  return newDiv; // this should be a complete row
};


function create_fields(type, data='') { // takes a dict of contact data and makes them into table fields/cells
  // console.log(`createfields; type: ${type}, data: ${data}`)
  if (type === 'select') { // contains the select checkbox
    let selectField = document.createElement('div')
    selectField.classList.add('table-field', 'checkbox')

    let selectBox = document.createElement('input') // the actual <input type='checkbox'>
    setAttributes(selectBox, {'type': 'checkbox', 'name': 'selected'})
    selectField.appendChild(selectBox)
    return selectField;

  } else if (type === 'spacer') { // used for spacing on the page, empty div in the column of the delete-selected button
    let spacerfield = document.createElement('div')
    spacerfield.classList.add(['table-field'])
    return spacerfield;

  } else { // uses the data to label and fill the table cell
    let field = document.createElement('div')
    field.classList.add(['table-field'])
    field.setAttribute('name', type)
    field.textContent = data
    return field;
  }
};


function set_checkboxes(params) {// node_list=false, toggle=false, checked=undefined) {  see below
  // if no list of nodes, then function selects all nodes on the document.
  // toggle = optionally toggle checked/unchecked
  // checked = set all nodes to checked(true) or unchecked(false)
  // console.log('checkbox')
  // console.log(`checked is ${params.checked}`)
  // console.log(params.toggle)
  if (typeof(params.node_list) === typeof(['array'])) {
    var nodes = params.node_list
  } else {
    var nodes = document.querySelectorAll("input[type='checkbox']")
  }
  // console.log(nodes)

  if (params.toggle) {
    let i = 0
    for (let node of nodes) {
      if (node.checked === false) { // if any node is unchecked, then i > 0
        // console.log('unchecked')
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
      // console.log(node)
      node.checked = params.checked // true or false!
    }
  }

};


function select_toggle() { // lazy solution to select-all button's onclick
  set_checkboxes({node_list: false, toggle: true, checked: undefined})
};


function generate() {
  // let D = new Date()
  // var doc_title = window.prompt('Please enter the spreadsheet title:', `Conversion ${D.getMonth() + 1}-${D.getDate()}-${D.getFullYear()}`) // placeholder format (January 1 2021))
  // if (doc_title === null) {
  //   alert('Generation cancelled.')
  //   return
  // }
  // console.log('sending request')
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
  // console.log('should have pinned')
}

var compileElement = document.querySelector('#compile-button') // adds listener for compile button
compileElement.addEventListener('click', function() {
  send_request('py_compile')
})
// console.log(compileElement)

// var deleteallElement = document.querySelector('#delete-all')
// deleteallElement.addEventListener('click', function() {
//   send_request('delete_all').then( () => {location.reload(true)})
//   // location.reload()
// })

  // for piece of info in response[company], make an appropriate div
