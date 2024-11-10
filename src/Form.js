import React, { useState } from 'react';
import emailjs from 'emailjs-com';

export default function Form() {
  const [fields, setFields] = useState([{ id: 1, value: '' }]); // Initial field
  const [showNewForm, setShowNewForm] = useState(false); // State to control which form to display
  const [itemName, setItemName] = useState(''); // State to store the item name for the newform
  const [name, setName] = useState(''); // State to store the name
  const [email, setEmail] = useState(''); // State to store the email
  const [ingredients, setIngredients] = useState([]);

  const handleInputChange = (id, event) => {
    const updatedFields = fields.map((field) =>
      field.id === id ? { ...field, value: event.target.value } : field
    );
    setFields(updatedFields);
  };

  const handlePrintClick = () =>{
    const ingredientsText = ingredients
    .map(ingredient => `${ingredient.name}: $${ingredient.price.toFixed(2)}`) 
    .join('\n');

  const templateParams = {
    user_name: name,
    user_email: email,
    ingredients_list: ingredientsText,
  };
  //console.log('Email:', email);
  //emailjs.send("service_ak1e34c", "template_nsc4jaa", templateParams, 'B9O6gWh7xb9ZfsCxH')
    //.then(response => {
      //console.log('Email sent successfully!', response.status, response.text);
   // })
   // .catch(error => {
    //  console.error('Error sending email:', error);
   // });

  setShowNewForm(false); 
};

  const handleFindIngredientsClick = async () => {
    const firstItemValue = fields[0]?.value || ''; 
    setItemName(firstItemValue); 
    try {
      const response = await fetch("http://127.0.0.1:8000/run-scraper", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          itemName: firstItemValue,
        }),
      });
  
      const data = await response.json();
      console.log(data); 
      if (Array.isArray(data.filtered_items)) {
        const updatedIngredients = data.filtered_items.map(ingredient => {
          console.log(ingredient)
          const price = parseFloat(ingredient.price?.replace?.('$', '').trim() ?? ingredient.price);  // Remove '$' and convert to number
          return {
            ...ingredient,
            price: !isNaN(price) ? price : 0, 
          };
        });
        setIngredients(updatedIngredients);
      } else {
        setIngredients(["word","col"]); 
      }
    } catch (error) {
      console.error('Error fetching ingredients:', error);
      setIngredients([]);
    }
    setShowNewForm(true);
  };
  

  return (
    <div className="form-container">
      {!showNewForm ? (
        <form className="form-content">
          <h2>Ingredient Finder</h2>
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
                  type="Item"
                  value={"Green Bean Casserole"}
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
        <form className="form-content">
          <div className="info-box">
              <p><strong>Name:</strong> {name}</p>
              <p><strong>Email:</strong> {email}</p>
          </div>
          <h2>{itemName}</h2> 
          <div className="form-field">
            <label>
              Ingredients:
              <div className="ingredient-list">
              {ingredients && Array.isArray(ingredients) && ingredients.length > 0 ? (
                ingredients.map((ingredient, index) => (
                  <div key={index} className="ingredient-item">
                    <span>{ingredient.name}</span>  
                    <span>${ingredient.price.toFixed(2)}</span> 
                  </div>
                ))
              ) : (
                <div>No ingredients found</div>
              )}
            </div>
            </label>
          </div>
          
          <div className="button-container">
            <div className="button-wrapper">
              <button type="button" onClick={() => setShowNewForm(false)} className="finding-button">
                Go Back
              </button>
            </div>
            {/*
            <div className="button-wrapper"> 
              <button type="button" 
              className="sending-button"
              onClick={handlePrintClick}
              >
                Print Ingredients
              </button>
            </div>
            */} 
          </div>
        </form>
      )}
    </div>
  );
}
