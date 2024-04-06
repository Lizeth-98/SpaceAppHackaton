import HashMap "mo:base/HashMap";
import Iter "mo:base/Iter";
import Nat32 "mo:base/Nat32";
import Text "mo:base/Text";
import Principal "mo:base/Principal";
import Debug "mo:base/Debug";
import Float "mo:base/Float";

actor Areas {
  type Area = {
		ph: Float;
		humedad: Float;
		nitrogeno: Float;
		fosforo: Float;
		potasio: Float;
	};

  type areaID = Nat32;
	stable var areaID: areaID = 0;

	let listaAreas = HashMap.HashMap<Text, Area>(0, Text.equal, Text.hash);

	private func generaAreaID() : Nat32 {
		areaID += 1;
		return areaID;
	};
	
	public query ({caller}) func whoami() : async Principal {
		return caller;
	};

	public shared (msg) func crearArea(ph: Float, humedad: Float , nitrogeno: Float , fosforo: Float , potasio: Float) : async () {
		let area = {nombre=nombre};

		listaAreas.put(Nat32.toText(generaAreaID()), area);
		Debug.print("Nueva área creada ID: " # Nat32.toText(areaID));
		return ();
	};

	public query func obtieneAreas () : async [(Text, Area)] {
		let areaIter : Iter.Iter<(Text, Area)> = listaAreas.entries();
		let areaArray : [(Text, Area)] = Iter.toArray(areaIter);
		Debug.print("Areas ");

		return areaArray;
	};

	public query func obtieneArea (id: Text) : async ?Area {
		let area: ?Area = listaAreas.get(id);
		return area;
	};

	public shared (msg) func actualizarArea (id: Text, ph: Float, humedad: Float , nitrogeno: Float ,fosforo: Float , potasio: Float) : async Bool {
		let area: ?Area = listaAreas.get(id);

		switch (area) {
			case (null) {
				return false;
			};
			case (?areaActual) {
				let nuevaArea: Area = {nombre=nombre};
				listaAreas.put(id, nuevaArea);
				Debug.print("Area actualizada: " # id);
				return true;
			};
		};

	};

	public func eliminarArea (id: Text) : async Bool {
		let area : ?Area = listaAreas.get(id);
		switch (area) {
			case (null) {
				return false;
			};
			case (_) {
				ignore listaAreas.remove(id);
				Debug.print("Área eliminadaD: " # id);
				return true;
			};
		};
	};


};