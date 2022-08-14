import React, {useState} from "react"

const FillInForm4 = ({transferSingleAnswer_4}) => {

    const [answer, setAnswer] = useState("");

    const handleChange = (e) => {
        setAnswer(e.target.value)
        console.log('from fill in form4', e.target.value)
        transferSingleAnswer_4(e.target.value)
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

export default FillInForm4