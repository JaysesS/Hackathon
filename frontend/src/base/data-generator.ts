export interface Data {
  id: number
  name: string
  position: string
  children: any
}

const createRandomPerson = (id) => {
  const data: Data = {
    id: id,
    name: id / 2 ? 'Пупа' : 'Лупа',
    position: 'Заводчанин',
    children: [
    ]
  }
  return data;
}

const AddChildToPerson = (person, child) => {
  person['children'].push(child);
  return person;
}

export function generateOrgChartData(depth: number = 3) {
  let lastId = 0;
  const data: Data = {
    id: lastId,
    name: 'Иван Иванович',
    position: 'Генеральный директор',
    children: [
    ]
  }
  lastId++;

  for (let i = 0; i < 3; i++) {
    const temp = createRandomPerson(++lastId);
    const rPerson = AddChildToPerson(temp, AddChildToPerson(createRandomPerson(++lastId), createRandomPerson(++lastId)));
    data['children'].push(rPerson);
  }

  return data
}

export function generateOrgChartDataFolded(depth: any, foldDepth: number) {
  const data = this.generateOrgChartData(depth)
  let tempNode = data
  for (let i = 0; i < foldDepth && tempNode.children; i++) {
    tempNode = tempNode.children[0]
  }
  tempNode._children = tempNode.children
  tempNode.children = null
  return data
}
