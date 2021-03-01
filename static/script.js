

function replace_brs(with_tags) { // a contenteditable div uses <br> tags instead of \n, so we need to replace those
  const regex = /<br>/;
  let no_tags = with_tags.replace(regex, '\n');
  return no_tags;
};


function send_request() {
  let target = document.getElementById('textarea');
  console.log(target.value);
  let sendthis = {
    message: replace_brs(target.value)
  };

  fetch(`${window.origin}/py_compile`, { // sending the request
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
      console.log(`data: ${data}`)
      for (let company of data) { // creates table rows and appends them to the table
        console.log(`company: ${company.name}`)
        let table = document.getElementById('companies-wrapper')
        table.appendChild(create_row(company))
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
  console.log(`createfields; type: ${type}, data: ${data}`)
  if (type === 'select') { // contains the select checkbox
    let selectField = document.createElement('div')
    selectField.classList.add('table-field', 'checkbox')

    let selectBox = document.createElement('input') // the actual <input type='checkbox'>
    setAttributes(selectBox, {'type': 'checkbox', 'name': 'selected'})
    selectField.checked = true // I want all new companies to default to being selected
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


function set_checkboxes(node_list=false, toggle=false, checked=undefined) { // see below
  // if no list of nodes, then function selects all nodes on the document.
  // toggle = optionally toggle checked/unchecked
  // checked = set all nodes to checked(true) or unchecked(false)
  console.log('checkbox')
  console.log(toggle)
  if (typeof(node_list) === typeof(['array'])) {
    var nodes = node_list
  } else {
    var nodes = document.querySelectorAll("input[type='checkbox']")
  }
  console.log(nodes)

  if (toggle) {
    let i = 0
    for (node of nodes) {
      if (node.checked === false) { // if any node is unchecked, then i > 0
        console.log('unchecked')
        i = i + 1
      }
    }

    if (i === 0) { // all nodes are checked
      for (node of nodes) {
        node.checked = false // uncheck them all
      }
    } else { // if at least one node is unchecked
      for (node of nodes) {
        node.checked = true // check them all
      }
    }
  }

  if (!(typeof(checked) === undefined)) { // if an argument was passed (bool)
    for (node in nodes) {
      node.checked = checked // true or false!
    }
  }

};


function select_toggle() { // lazy solution to select-all button's onclick
  set_checkboxes(node_list=false, toggle=true, checked=undefined)
};



  // for piece of info in response[company], make an appropriate div
