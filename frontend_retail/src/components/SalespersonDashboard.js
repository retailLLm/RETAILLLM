import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';


const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
`;

const DashboardWrapper = styled.div`
  display: flex;
  flex-direction: column;
  width: 80%;
  max-width: 1200px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
`;

const SectionTitle = styled.h2`
  margin-bottom: 20px;
  color: #007bff;
`;

const DataSection = styled.div`
  margin-bottom: 40px;
`;

const DataList = styled.ul`
  list-style: none;
  padding: 0;
`;

const DataItem = styled.li`
  margin-bottom: 10px;
  font-size: 16px;
`;

const SalesDashboardPage = () => {
  const [productAvailability, setProductAvailability] = useState([]);
  const [salesTrends, setSalesTrends] = useState([]);
  const [salesPerformance, setSalesPerformance] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const availabilityResponse = await axios.get('YOUR_BACKEND_ENDPOINT/availability');
        const trendsResponse = await axios.get('YOUR_BACKEND_ENDPOINT/trends');
        const performanceResponse = await axios.get('YOUR_BACKEND_ENDPOINT/performance');
        
        setProductAvailability(availabilityResponse.data);
        setSalesTrends(trendsResponse.data);
        setSalesPerformance(performanceResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
    
      <PageWrapper>
        <DashboardWrapper>
          <DataSection>
            <SectionTitle>Product Availability</SectionTitle>
            <DataList>
              {productAvailability.map((item, index) => (
                <DataItem key={index}>{item}</DataItem>
              ))}
            </DataList>
          </DataSection>
          <DataSection>
            <SectionTitle>Sales Trends</SectionTitle>
            <DataList>
              {salesTrends.map((item, index) => (
                <DataItem key={index}>{item}</DataItem>
              ))}
            </DataList>
          </DataSection>
          <DataSection>
            <SectionTitle>Sales Performance</SectionTitle>
            <DataList>
              {salesPerformance.map((item, index) => (
                <DataItem key={index}>{item}</DataItem>
              ))}
            </DataList>
          </DataSection>
        </DashboardWrapper>
      </PageWrapper>
    </div>
  );
};

export default SalesDashboardPage;
