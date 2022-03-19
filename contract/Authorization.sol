// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Authorization {

   address payable public owner;
   mapping(address => bool) AuthorizeUser;

   event AuthorizationGiven(
      bool value,
      address user
   );

   modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

   constructor() payable {
        owner = payable(msg.sender);
   }

   modifier OnlyAuthorizeUser() {
      require(msg.sender == owner || AuthorizeUser[msg.sender] );
      _;
   }
   
   function authorize_user() 
   public 
   OnlyAuthorizeUser
   {  
      AuthorizeUser[msg.sender] = true;
      emit AuthorizationGiven(true,msg.sender);
   }
}