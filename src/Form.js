import React, { useState } from 'react';

export default function Form() {
  const [fields, setFields] = useState([{ id: 1, value: '' }]); // Initial field
  const [showNewForm, setShowNewForm] = useState(false); // State to control which form to display
  const [itemName, setItemName] = useState(''); // State to store the item name for the newform
  const [name, setName] = useState(''); // State to store the name
  const [email, setEmail] = useState(''); // State to store the email
  const [ingredients, setIngredients] = useState([]);

  const testData = [{name: 'Pizza', price: 500}, {name: 'Mac and cheese', price: 2.50}]
  
  
  const addField = () => {
    setFields([...fields, { id: fields.length + 1, value: '' }]);
  };

  const handleInputChange = (id, event) => {
    const updatedFields = fields.map((field) =>
      field.id === id ? { ...field, value: event.target.value } : field
    );
    setFields(updatedFields);
  };

  const handleFindIngredientsClick = async () => {
    // Set the first item's value as the item name for the new form
    const firstItemValue = fields[0]?.value || ''; // Use first item's value or empty string if no value
    setItemName(firstItemValue); // Store the item name
    setShowNewForm(true); // Show the new form
    try {
      const response = await fetch(`${process.env.PUBLIC_URL}/ingredients.txt`);
      const text = await response.text();
      
      // Process each line and split into objects
      const lines = text.split('\n').filter(line => line.trim() !== '');
      const ingredientsArray = lines.map(line => {
        const [name, price] = line.split(','); // Assuming name and price are separated by a comma
        return { name: name.trim(), price: parseFloat(price.trim()) };
      });
      
      setIngredients(ingredientsArray);
    } catch (error) {
      console.error('Error fetching ingredients:', error);
    }
  };

  return (
    
    <div className="form-container">
      {!showNewForm ? (
        // The initial form
        <form className="form-content">
          <h2>Recepie Finder</h2>
          <div className="form-field">
            <label>
              Name:
              <input type="text" name="name" value={name} onChange={(e) =>setName(e.target.value) }/>
            </label>
          </div>

          <div className="form-field">
            <label>
              Email:
              <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
            </label>
          </div>

          {fields.map((field) => (
            <div key={field.id} className="form-field">
              <label>
                Item:
                <input
                  type="text"
                  value={field.value}
                  onChange={(e) => handleInputChange(field.id, e)}
                />
              </label>
            </div>
          ))}

          <div className="button-container">
            <div className="button-wrapper">
              <button
                type="button"
                onClick={handleFindIngredientsClick}
                className="finding-button"
              >
                Find Ingredients
              </button>
            </div>
          </div>
        </form>
      ) : (
        // The new form to show after button press
        
        <form className="form-content">
          {/* Box displaying Name and Email */}
          <div className="info-box">
              <p><strong>Name:</strong> {name}</p>
              <p><strong>Email:</strong> {email}</p>
          </div>
          <h2>{itemName}</h2> {/* Display the item name here */}
          <div className="form-field">
            <label>
              Ingredients:
              <ul>
              {ingredients.map((ingredient, index) => (
              <li key={index}>
              {ingredient.name} - ${ingredient.price.toFixed(2)}
               </li>
               ))}
              </ul>
              {/* <input type="text" name="newInfo" /> */}
            </label>
          </div>
          
          <div className="button-container">
            <div className="button-wrapper">
              <button type="button" onClick={() => setShowNewForm(false)} className="finding-button">
                Go Back
              </button>
            </div>
            <div className="button-wrapper"> {/*onClick-{()=> event that put all ingreditent to email}*/}
              <button type="button" 
              className="sending-button">
                Print Ingredients
              </button>
            </div>
          </div>
        </form>
      )}
    </div>
  );
}