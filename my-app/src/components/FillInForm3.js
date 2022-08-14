import React, {useState} from "react"

const FillInForm3 = ({transferSingleAnswer_3}) => {

    const [answer, setAnswer] = useState("");

    const handleChange = (e) => {
        setAnswer(e.target.value)
        console.log('from fill in form3', e.target.value)
        transferSingleAnswer_3(e.target.value)
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

export default FillInForm3
