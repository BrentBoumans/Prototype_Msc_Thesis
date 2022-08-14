import React from 'react'

const InstructionBox = ({exerciseToShow}) => {
  return (
    <div className='instructionBox'>
      <span className='bold'>Conjugate: </span> <span className='bold'>{exerciseToShow.verb}</span>
    </div>
  )
}
export default InstructionBox
