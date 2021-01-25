// Fit the D2 measurement and compare the field with the magic spreadsheet one

void fit_d2(double current){

  Double_t I,B;
  Double_t x[100];  
  Double_t y[100];  

  string dummy;
  Int_t i = 0;

  ifstream is;
  is.open("measurement/d2_center_down.txt");
  //is.open("measurement/d1_up.txt");

  while (is.good())
    {
      is >> I >> B;
      y[i]=I;
      x[i]=B;

      i++;

    }
  is.close();

  cout << "New fit: " << endl;
  TGraph* graph = new TGraph(i,x,y);
  graph->Fit("pol3");
  graph->Draw("A*");

  TGraph* graph = new TGraph(i,y,x);
  graph->GetXaxis()->SetTitle("Current [A]");
  graph->GetYaxis()->SetTitle("B [T]");
  graph->SetTitle("D2");
  graph->Fit("pol3");
  graph->Draw("A*");
  c1->SaveAs("B_vs_I.png");

  // Magic Spreadsheet
  TF1 *func1=new TF1("func1","[0]+[1]*x+[2]*x^2+[3]*x^3",0,0.9);
  func1->SetParameters(0,253.91,-55.998,39.59);
  func1->SetLineColor(1);  //black
  func1->Draw();

  // Fit
  TF1 *func2=new TF1("func2","[0]+[1]*x+[2]*x^2+[3]*x^3",0,0.9);
  func2->SetParameters(-0.62,239.699,-3.96478,4.43363);
  func2->SetLineColor(2);  //red
  func2->Draw("same");

  cout << "Magic: I=100A, B=" << func1->GetX(100,0,2) << endl;
  cout << "Fit:   I=100A, B=" << func2->GetX(100,0,2) << endl;
  cout << (func2->GetX(100,0,2)-func1->GetX(100,0,2))/func2->GetX(100,0,2)*100 << "%" << endl;
  
  cout << "Magic: I=142.66A, B=" << func1->GetX(142.66,0,2) << endl;
  cout << "Fit:   I=142.66A, B=" << func2->GetX(142.66,0,2) << endl;
  cout << (func2->GetX(142.66,0,2)-func1->GetX(142.66,0,2))/func2->GetX(142.66,0,2)*100 << "%" << endl;

  cout << "Magic: I=160.8A, B=" << func1->GetX(160.8,0,2) << endl;
  cout << "Fit:   I=160.8A, B=" << func2->GetX(160.8,0,2) << endl;
  cout << (func2->GetX(160.8,0,2)-func1->GetX(160.8,0,2))/func2->GetX(160.8,0,2)*100 << "%" << endl;

  cout << "Magic: I=180.7A, B=" << func1->GetX(180.7,0,2) << endl;
  cout << "Fit:   I=180.7A, B=" << func2->GetX(180.7,0,2) << endl;
  cout << (func2->GetX(180.7,0,2)-func1->GetX(180.7,0,2))/func2->GetX(180.7,0,2)*100 << "%" << endl;

  cout << "Magic: I=200A, B=" << func1->GetX(200,0,2) << endl;
  cout << "Fit:   I=200A, B=" << func2->GetX(200,0,2) << endl;
  cout << (func2->GetX(200,0,2)-func1->GetX(200,0,2))/func2->GetX(200,0,2)*100 << "%" << endl;

  cout << "Magic: I=210.61A, B=" << func1->GetX(210.61,0,2) << endl;
  cout << "Fit:   I=210.61A, B=" << func2->GetX(210.61,0,2) << endl;
  cout << (func2->GetX(210.61,0,2)-func1->GetX(210.61,0,2))/func2->GetX(210.61,0,2)*100 << "%" << endl;

  cout << "Magic: I=240A, B=" << func1->GetX(240,0,2) << endl;
  cout << "Fit:   I=240A, B=" << func2->GetX(240,0,2) << endl;
  cout << (func2->GetX(240,0,2)-func1->GetX(240,0,2))/func2->GetX(240,0,2)*100 << "%" << endl;

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


  cout << "Input current:" << endl;
  fit(current);


  Double_t I;

  // 3-140
  I=142.664993;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;
  I=69.987999;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;


  I=304.98999;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;

  I=91.484001;
  cout << "Magic: I= " << I << ", B= " << func1->GetX(I,0,2) << endl;
  cout << "Fit:   I= " << I << ", B= " << func2->GetX(I,0,2) << endl;


  cout << "9883,10243:" << endl;
  fit(71.917999);
  cout << "9885:" << endl;
  fit(76.400002);
  cout << "9886:" << endl;
  fit(86.972);

  cout << "ok, and higher mom.. emittance = 3 " << endl;
  cout << "170, 9911:" << endl;
  fit(86.543999);
  cout << "200, 9910:" << endl;
  fit(94.921997);
  cout << "240, 9909:" << endl;
  fit(110.821999);

  cout << "3,6,10-200" << endl;
  cout << "9760, 3-200" << endl;
  fit(94.924004);
  cout << "9761, 6-200" << endl;
  fit(98.0);
  cout << "9763, 10-200" << endl;
  fit(108.019997);


  cout << "6,10-240:" << endl;
  cout << "10404, 6-240" << endl;
  fit(110.001999);
  cout << "10405, 10-240" << endl;
  fit(119.989998);


}
 
void fit(double current) {

  double correction;

  cout << "Magic: I= " << current << "A, B=" << func1->GetX(current,0,2) << endl;
  cout << "Fit:   I= " << current << "A, B=" << func2->GetX(current,0,2) << endl;

  correction= (func2->GetX(current,0,2)-func1->GetX(current,0,2))/func2->GetX(current,0,2);
  cout << correction*100 << "%" << endl;
  cout << "New current: " << current-current*correction << endl << endl;

}

