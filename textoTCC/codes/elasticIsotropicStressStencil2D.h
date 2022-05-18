void FDM2E2T_elasticIsotropic2D(float *Vx,float *Vz,float *Txx,float *Tzz,float *Txz,float *rho, 
                                float *M,float *L,int nxx,int nzz,float dt,float dx,float dz) 
{   
    for(int index = 0; index < nxx*nzz; index++) 
    {                  
        int ii = (int) index / nxx;      // indicador de linhas  --> z
        int jj = (int) index % nxx;      // indicador de colunas --> x

        if((ii >= 0) && (ii < nzz-1) && (jj >= 0) && (jj < nxx-1)) 
        {
            float dVx_dx = (Vx[(jj+1) + ii*nxx] - Vx[jj + ii*nxx])/dx;
            float dVz_dz = (Vz[jj + (ii+1)*nxx] - Vz[jj + ii*nxx])/dz;     

            Txx[index] += dt*((L[index] + 2.0f*M[index])*dVx_dx + L[index]*dVz_dz);   
            Tzz[index] += dt*((L[index] + 2.0f*M[index])*dVz_dz + L[index]*dVx_dx);
        }
    
        if((ii > 0) && (ii < nzz) && (jj > 0) && (jj < nxx)) 
        {
            float dVz_dx = (Vz[jj + ii*nxx] - Vz[(jj-1) + ii*nxx])/dx;
            float dVx_dz = (Vx[jj + ii*nxx] - Vx[jj + (ii-1)*nxx])/dz;
            
            float Mxz = powf(0.25f*(1.0f/M[jj + (ii+1)*nxx] + 1.0f/M[(jj+1) + ii*nxx] 
                                  + 1.0f/M[(jj+1) + (ii+1)*nxx] + 1.0f/M[jj + ii*nxx]),-1.0f); 

            Txz[index] += dt*Mxz*(dVx_dz + dVz_dx);            
        }          
    }

    for(int index = 0; index < nxx*nzz; index++) 
    {              
        int ii = (int) index / nxx;      // indicador de linhas  --> z
        int jj = (int) index % nxx;      // indicador de colunas --> x

        if((ii >= 0) && (ii < nzz-1) && (jj > 0) && (jj < nxx)) 
        {
            float dTxx_dx = (Txx[jj + ii*nxx] - Txx[(jj-1) + ii*nxx])/dx;
            float dTxz_dz = (Txz[jj + (ii+1)*nxx] - Txz[jj + ii*nxx])/dz
            
            float rhox = 0.5f*(rho[(jj+1) + ii*nxx] + rho[jj + ii*nxx]);

            Vx[index] += dt/rhox*(dTxx_dx + dTxz_dz);  
        }
      
        if((ii > 0) && (ii < nzz) && (jj >= 0) && (jj < nxx-1)) 
        {
            float dTxz_dx = (Txz[(jj+1) + ii*nxx] - Txz[jj + ii*nxx])/dx;
            float dTzz_dz = (Tzz[jj + ii*nxx] - Tzz[jj + (ii-1)*nxx])/dz;
 
            float rhoz = 0.5f*(rho[jj + (ii+1)*nxx] + rho[jj + ii*nxx]);

            Vz[index] += dt/rhoz*(dTxz_dx + dTzz_dz); 
        }
    }
}
