import HashMap "mo:base/HashMap";
import Iter "mo:base/Iter";
import Nat32 "mo:base/Nat32";
import Text "mo:base/Text";
import Principal "mo:base/Principal";
import Debug "mo:base/Debug";
import Float "mo:base/Float";

actor Areas {
	type Area = {
		ph : Float;
		humedad : Float;
		nitrogeno : Float;
		fosforo : Float;
		potasio : Float;
	};

	type areaID = Nat32;
	stable var areaID : areaID = 0;

	let listaAreas = HashMap.HashMap<Text, Area>(0, Text.equal, Text.hash);

	private func generaAreaID() : Nat32 {
		areaID += 1;
		return areaID;
	};

	public shared (msg) func crearArea(ph : Float, humedad : Float, nitrogeno : Float, fosforo : Float, potasio : Float) : async () {
		let area = {
			ph = ph;
			humedad = humedad;
			nitrogeno = nitrogeno;
			fosforo = fosforo;
			potasio = potasio;
		};

		listaAreas.put(Nat32.toText(generaAreaID()), area);
		Debug.print("Nueva área creada ID: " # Nat32.toText(areaID));
		return ();
	};

	public query func obtieneAreas() : async [(Text, Area)] {
		let areaIter : Iter.Iter<(Text, Area)> = listaAreas.entries();
		let areaArray : [(Text, Area)] = Iter.toArray(areaIter);
		Debug.print("Areas ");

		return areaArray;
	};

};
