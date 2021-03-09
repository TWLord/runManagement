// Compare dipole currents with Magic spreadsheet and new Dipole fit

{

  // Magic Spreadsheet
  TF1 *func1=new TF1("func1","[0]+[1]*x+[2]*x^2+[3]*x^3",0,1.6);
  func1->SetParameters(0,253.91,-55.998,39.59);

  // Fit
  TF1 *func2=new TF1("func2","[0]+[1]*x+[2]*x^2+[3]*x^3",0,1.6);
  func2->SetParameters(0,253.91,-55.998,39.59);


  cout << "Magic: I=200A, B=" << func1->GetX(200,0,2) << endl;
  cout << "Fit:   I=200A, B=" << func2->GetX(200,0,2) << endl;
  cout << (func2->GetX(200,0,2)-func1->GetX(200,0,2))/func2->GetX(200,0,2)*100 << "%" << endl;

  cout << "Magic: I=350A, B=" << func1->GetX(350,0,2) << endl;
  cout << "Fit:   I=350A, B=" << func2->GetX(350,0,2) << endl;
  cout << (func2->GetX(350,0,2)-func1->GetX(350,0,2))/func2->GetX(350,0,2)*100 << "%" << endl;

  cout << "Magic: I=400A, B=" << func1->GetX(400,0,2) << endl;
  cout << "Fit:   I=400A, B=" << func2->GetX(400,0,2) << endl;
  cout << (func2->GetX(400,0,2)-func1->GetX(400,0,2))/func2->GetX(400,0,2)*100 << "%" << endl;

  cout << "B=1T, DeltaI=" << func1(1,0,2)-func2(1,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.1,0,2)-func2(1.1,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.2,0,2)-func2(1.2,0,2) << endl;
  cout << "B=1T, DeltaI=" << func1(1.3,0,2)-func2(1.3,0,2) << endl;


  Double_t I;

  I=142.664993A;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;

  I=69.987999;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;


}
 
