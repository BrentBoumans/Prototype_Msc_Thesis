import React, {useState} from "react"

const FillInForm = ({transferSingleAnswer}) => {

  const [answer, setAnswer] = useState("");
  
  // console.log(answer)

  const handleChange = (e) => {
    setAnswer(e.target.value)
    console.log(answer)
    transferSingleAnswer(answer)
    // FillInForm.props.handleAnswerList(answer)
  }

  return (
    <form className='fillInForm'>
        <div className='fillInForm-control'>
            <input type='text' value = {answer} placeholder='TBC' onChange={handleChange}/> 
        </div>
    </form>
  )
}

export default FillInForm
