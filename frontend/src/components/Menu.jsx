import Navbar from './Navbar';
import Prompts from "./Prompts";

import styles from "../style";
import { footerLinks, prompts, socialMedia } from "../constants";

import React, { useState } from 'react';

export const Menu = () =>  {
  const [activePrompt, setActivePrompt] = useState(null); // State variable to track the active prompt
  const handleClick = (id) => {
    setActivePrompt(id);
};
  return(
    <section id="menu" className={`h-full flex flex-col relative`}>
      <Navbar children={"menu-nav"}/>
      
      <div className={`min-h-[680px] max-h-[680px] flex flex-col px-4 py-6 overflow-y-auto`}>
        <div className={`${styles.flexCenter} mb-6`}>
          <button className={`w-[200px] h-[55px] rounded-[11px] outline-none bg-main_black button_shadow`}>
            <h4 className={`${styles.whiteNormal} mr-2 text-[19px]`}>New Chat</h4>
          </button>
        </div>
        {prompts.map((prompt, index) => (
          <div key={prompt.category} className={`${index !== prompt.length - 1 ? "mb-4" : ""}`}>
            <h4 className={`${styles.grayMedium} text-[16px] tracking-tight mx-4`}>{prompt.category}</h4>
            <div className={`${styles.flexCenter} flex-col relative`}>
              {prompt.Allprompts.map((prom) => (<Prompts key = {prom.id} {...prom} isActive={activePrompt === prom.id} onClick={handleClick}/>))}
            </div>
          </div>
        ))}
      </div>

      <div className={`mx-4 w-[90%] h-[2px] my-2 bg-text_color`} />
      <div className='px-4 py-2'>
          <div className={`${styles.flexEnd} w-full mb-4 mt-3`}>
            <h4 className={`${styles.blackBold} text-[17px]`}>Join us</h4>
            <div className="flex flex-row">
              {socialMedia.map((social, index) => (
                <img key={social.id} src={social.icon} alt={social.id} 
                  className={`w-[27px] object-contain cursor-pointer ${index !== social.length - 1 ? "mr-1.5" : "mr-0"}`}
                />
              ))}
            </div>
          </div>
          <div className={`${styles.flexBetween} flex-wrap w-full my-3`}>
                {footerLinks.map((footerLink, index) => (
                  <a href={footerLink.link} className={`${styles.grayMedium} text-[13px]`}>{footerLink.name}</a>
                ))}
          </div>
      </div>
    </section>
  )
}


export default Menu;
