import React, {useState} from "react"

const FillInForm2 = ({transferSingleAnswer_2}) => {

    const [answer, setAnswer] = useState("");

    const handleChange = (e) => {
        setAnswer(e.target.value)
        console.log('from fill in form2', e.target.value)
        transferSingleAnswer_2(e.target.value)
        // FillInForm.props.handleAnswerList(answer)
      }

  return (
    <form className='fillInForm'>
        <div className='fillInForm-control'>
            <input type='text' value = {answer} placeholder='type here' onChange={handleChange}/> 
        </div>
    </form>
  )
}

export default FillInForm2
