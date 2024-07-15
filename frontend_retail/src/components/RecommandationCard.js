import React from 'react';
import styled from 'styled-components';


const Card = styled.div`
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin: 10px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Title = styled.h3`
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #007bff;
`;

const Price = styled.p`
  color: #007bff;
  font-weight: bold;
  font-size: 18px;
  margin: 10px 0;
`;

const Rating = styled.p`
  color: #f39c12;
  font-size: 16px;
  margin: 10px 0;
`;



const RecommendationCard = ({ recommendation }) => {
 

 

  return (
    <Card>
      <Title>{recommendation.title}</Title>
      <Price>${recommendation.price}</Price>
      <Rating>Rating: {recommendation.rating}</Rating>
     
    </Card>
  );
};

export default RecommendationCard;
