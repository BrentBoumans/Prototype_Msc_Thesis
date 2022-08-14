import React from 'react'
import {useState} from 'react';

const RSSelector = ({transferRSSelection}) => {

    const [on, setOn] = useState(true)
    
    const handleToggle = (e) =>  {
        e.preventDefault();
        console.log('intern is the value of on being changed')
        console.log('before changing the value of on = ', on)
        setOn(!on)
        console.log('before changing the value of on = ', on)
        transferRSSelection()
    }
         
  return (
    <div className = 'rs-box'>
      <input
        checked = {on}
        onChange= {handleToggle}
        className="react-switch-checkbox"
        id={`react-switch-new`}
        type="checkbox"
      />
      <label
        style={{background: on && '#06D6A0'}}
        className="react-switch-label"
        htmlFor={`react-switch-new`}
      >
        <span className={`react-switch-button`} />
      </label>
    </div>
  )
}

export default RSSelector
