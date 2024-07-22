db = db.getSiblingDB('qc_demo'); 
db.createCollection('spec'); 
// Insert initial data

db.spec.insertMany([
  { spec_id: "sp01",
     process: "side_lap",
     item_1:{spec_name:"width",spec:10.0,spec_max:11.0,spec_min:9.0,point:1,method:1},
     item_2:{spec_name:"width_para",spec:1,spec_max:1.1,spec_min:0.9,point:3,method:2}
    },
    { spec_id: "sp02",
      process: "outgoing",
      item_1:{spec_name:"width",spec:5.0,spec_max:6.0,spec_min:4.0,point:1,method:1},
      item_2:{spec_name:"width_para",spec:0.1,spec_max:0.15,spec_min:0.05,point:3,method:2}
     },
     { spec_id: "sp03",
      process: "od_grinding",
      item_1:{spec_name:"od_dia",spec:15.0,spec_max:16.0, spec_min:14.0, point:1,method:1},
      item_2:{spec_name:"od_taper",spec:0.1,spec_max:0.15,spec_min:0.05,point:3,method:3}
     },
     { spec_id: "sp04",
      process: "Outgoing",
      item_1:{spec_name:"od_dia",spec:5.0,spec_max:6.0,spec_min:4.0,point:1,method:1},
      item_2:{ spec_name:"od_taper",spec:0.1,spec_max:0.15,spec_min:0.05,point:3,method:3}
     },
]);