const classNames = {
  TODO_ITEM: 'todo-container',
  TODO_CHECKBOX: 'todo-checkbox',
  TODO_TEXT: 'todo-text',
  TODO_DELETE: 'todo-delete',
}

const list = document.getElementById('todo-list')
const itemCountSpan = document.getElementById('item-count')
const uncheckedCountSpan = document.getElementById('unchecked-count')

function newTodo() {
	let itemContainer = document.createElement('li');
	let itemCheckbox = document.createElement('input');
	let itemText = document.createElement('span');
	let itemDelete = document.createElement('button');
	
	itemContainer.classList.add(classNames['TODO_ITEM']);
	itemCheckbox.classList.add(classNames['TODO_CHECKBOX']);
	itemText.classList.add(classNames['TODO_TEXT']);
	itemDelete.classList.add(classNames['TODO_DELETE']);
	
	
	itemCheckbox.type = 'checkbox'
	itemCheckbox.onclick = function() {
		if (itemCheckbox.checked === false){
			uncheckedCountSpan.innerHTML = Number(uncheckedCountSpan.innerHTML) + 1;
		} else {
			uncheckedCountSpan.innerHTML = Number(uncheckedCountSpan.innerHTML) - 1;
		}
		
	}
	
	itemDelete.appendChild(document.createTextNode('Delete'));
	itemDelete.onclick = function (){
		list.removeChild(itemContainer);
		itemCountSpan.innerHTML = Number(itemCountSpan.innerHTML) - 1;
		uncheckedCountSpan.innerHTML = Number(uncheckedCountSpan.innerHTML) - 1;
	}
	

	itemText.appendChild(document.createTextNode('Uus asi'));
	itemContainer.appendChild(itemCheckbox);
	itemContainer.appendChild(itemText);
	itemContainer.appendChild(itemDelete);
	list.appendChild(itemContainer);
	
	itemCountSpan.innerHTML = Number(itemCountSpan.innerHTML) + 1;
	uncheckedCountSpan.innerHTML = Number(uncheckedCountSpan.innerHTML) + 1;
}





