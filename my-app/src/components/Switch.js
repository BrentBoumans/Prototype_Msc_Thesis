import React from 'react'

const Switch = ({traRSToggled, onToggle}) => {
  return (
    <>
        <span className='textboxTRS'>
            Recommender System A 
        </span>
        <label className='switch'>
        <input type= "checkbox" checked={!traRSToggled} onChange={onToggle}/>
        <span className='slider'/>
        </label>
        <span className = 'textboxADA'>
            Recommender System B
        </span>
        
    </>
  )
}


export default Switch
